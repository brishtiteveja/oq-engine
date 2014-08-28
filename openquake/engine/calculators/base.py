# Copyright (c) 2010-2014, GEM Foundation.
#
# OpenQuake is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# OpenQuake is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with OpenQuake.  If not, see <http://www.gnu.org/licenses/>.

"""Base code for calculator classes."""

from openquake.engine import logs
from openquake.engine.performance import EnginePerformanceMonitor
from openquake.engine.utils import tasks, config

from openquake.commonlib.source import SourceCollector


class Calculator(object):
    """
    Base class for all calculators.

    :param job: :class:`openquake.engine.db.models.OqJob` instance.
    """

    #: The core calculation Celery task function, which accepts the arguments
    #: generated by :func:`task_arg_gen`.
    core_calc_task = None

    def __init__(self, job):
        self.job = job
        self.num_tasks = None
        self._task_args = []
        # parameters from openquake.cfg
        self.concurrent_tasks = int(
            config.get('celery', 'concurrent_tasks'))
        self.max_input_weight = float(
            config.get('hazard', 'max_input_weight'))
        self.max_output_weight = float(
            config.get('hazard', 'max_output_weight'))
        SourceCollector.POINT_SOURCE_WEIGHT = float(
            config.get('hazard', 'point_source_weight'))

    def monitor(self, operation=None):
        """
        Return a :class:`openquake.engine.performance.EnginePerformanceMonitor`
        instance, associated to the operation and with tracing and flushing
        enabled.

        :param str operation: the operation to monitor
        """
        return EnginePerformanceMonitor(
            operation, self.job.id, tracing=True, flush=True)

    def task_arg_gen(self):
        """
        Generator function for creating the arguments for each task.

        Subclasses must implement this.
        """
        raise NotImplementedError

    def parallelize(self, task_func, task_arg_gen, task_completed):
        """
        Given a callable and a task arg generator, build an argument list and
        apply the callable to the arguments in parallel. The order is not
        preserved.

        Every time a task completes the method .task_completed() is called.

        :param task_func: a `celery` task callable
        :param task_args: an iterable over positional arguments

        NB: if the environment variable OQ_NO_DISTRIBUTE is set the
        tasks are run sequentially in the current process.
        """
        oqm = tasks.OqTaskManager(task_func, logs.LOG.progress)
        with self.monitor('submitting %s' % task_func.__name__):
            for args in task_arg_gen:
                oqm.submit(*args)
        oqm.aggregate_results(lambda acc, val: task_completed(val), None)

    def task_completed(self, task_result):
        """
        Method called when a task is completed. It can be overridden
        to aggregate the partial results of a computation.

        :param task_result: the result of the task
        """
        pass

    def pre_execute(self):
        """
        Override this method in subclasses to record pre-execution stats,
        initialize result records, perform detailed parsing of input data, etc.
        """

    @EnginePerformanceMonitor.monitor
    def execute(self):
        """
        Run the core_calc_task in parallel, by passing the arguments
        provided by the .task_arg_gen method. By default it uses the
        parallelize distribution, but it can be overridden is subclasses.
        """
        self.parallelize(self.core_calc_task,
                         self.task_arg_gen(),
                         self.task_completed)

    def post_execute(self):
        """
        Override this method in subclasses to any necessary post-execution
        actions, such as the consolidation of partial results.
        """

    def post_process(self):
        """
        Override this method in subclasses to perform post processing steps,
        such as computing mean results from a set of curves or plotting maps.
        """

    def _get_outputs_for_export(self):
        """
        Util function for getting :class:`openquake.engine.db.models.Output`
        objects to be exported.
        """
        raise NotImplementedError

    def _do_export(self, output_id, export_dir, export_type):
        """
        Perform a single export.
        """
        raise NotImplementedError()

    def export(self, *args, **kwargs):
        """
        If requested by the user, automatically export all result artifacts to
        the specified format. (NOTE: The only export format supported at the
        moment is NRML XML.

        :param exports:
            Keyword arg. List of export types.
        :returns:
            A list of the export filenames, including the absolute path to each
            file.
        """
        exported_files = []

        with logs.tracing('exports'):
            if 'exports' in kwargs:
                outputs = self._get_outputs_for_export()

                for export_type in kwargs['exports']:
                    for output in outputs:
                        with self.monitor('exporting %s to %s'
                                          % (output.output_type, export_type)):
                            fname = self._do_export(
                                output.id,
                                self.job.calculation.export_dir,
                                export_type
                            )
                            logs.LOG.info('exported %s', fname)
                            exported_files.append(fname)

        return exported_files

    def clean_up(self, *args, **kwargs):
        """Implement this method in subclasses to perform clean-up actions
           like garbage collection, etc."""
