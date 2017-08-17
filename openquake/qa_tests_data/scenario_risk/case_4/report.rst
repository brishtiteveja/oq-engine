Scenario Risk for Nepal with 20 assets
======================================

================================================ ========================
tstation.gem.lan:/mnt/ssd/oqdata/calc_14503.hdf5 Thu Aug 17 11:49:00 2017
checksum32                                       2,254,713,843           
engine_version                                   2.6.0-gitbdd9d17        
================================================ ========================

num_sites = 20, num_imts = 1

Parameters
----------
=============================== ==================
calculation_mode                'scenario_risk'   
number_of_logic_tree_samples    0                 
maximum_distance                {'default': 500.0}
investigation_time              None              
ses_per_logic_tree_path         1                 
truncation_level                3.0               
rupture_mesh_spacing            15.0              
complex_fault_mesh_spacing      15.0              
width_of_mfd_bin                None              
area_source_discretization      None              
ground_motion_correlation_model None              
random_seed                     42                
master_seed                     0                 
avg_losses                      False             
=============================== ==================

Input files
-----------
======================== ==========================================================================
Name                     File                                                                      
======================== ==========================================================================
exposure                 `exposure_model.xml <exposure_model.xml>`_                                
job_ini                  `job.ini <job.ini>`_                                                      
rupture_model            `fault_rupture.xml <fault_rupture.xml>`_                                  
structural_vulnerability `structural_vulnerability_model.xml <structural_vulnerability_model.xml>`_
======================== ==========================================================================

Composite source model
----------------------
========= ====== ================= =============== ================
smlt_path weight source_model_file gsim_logic_tree num_realizations
========= ====== ================= =============== ================
b_1       1.000  `fake <fake>`_    trivial(1)      1/1             
========= ====== ================= =============== ================

Required parameters per tectonic region type
--------------------------------------------
====== ================= =========== ======================= =================
grp_id gsims             distances   siteparams              ruptparams       
====== ================= =========== ======================= =================
0      ChiouYoungs2008() rjb rrup rx vs30 vs30measured z1pt0 dip mag rake ztor
====== ================= =========== ======================= =================

Realizations per (TRT, GSIM)
----------------------------

::

  <RlzsAssoc(size=1, rlzs=1)
  0,ChiouYoungs2008(): ['<0,b_1~b1,w=1.0>']>

Informational data
------------------
================ ================
hostname         tstation.gem.lan
require_epsilons True            
================ ================

Exposure model
--------------
=============== ========
#assets         20      
#taxonomies     4       
deductibile     relative
insurance_limit relative
=============== ========

========================== ===== ====== === === ========= ==========
taxonomy                   mean  stddev min max num_sites num_assets
Adobe                      1.000 0.0    1   1   3         3         
Stone-Masonry              1.000 0.0    1   1   4         4         
Unreinforced-Brick-Masonry 1.000 0.0    1   1   5         5         
Wood                       1.000 0.0    1   1   8         8         
*ALL*                      1.000 0.0    1   1   20        20        
========================== ===== ====== === === ========= ==========

Slowest operations
------------------
======================= ========= ========= ======
operation               time_sec  memory_mb counts
======================= ========= ========= ======
reading exposure        0.010     0.0       1     
filtering sites         0.004     0.0       1     
saving gmfs             0.003     0.0       1     
computing gmfs          0.001     0.0       1     
building riskinputs     8.383E-04 0.0       1     
building epsilons       5.395E-04 0.0       1     
reading site collection 5.007E-06 0.0       1     
======================= ========= ========= ======