

from lib.__init__ import *
from lib.forward_model.scanner_template import ScannerTemplate,\
                                               default_scanner_parallel


# -----------------------------------------------------------------------------
# Step 1: Specify dataset parameter:

bags_to_create = range(1, 10)                  # Number of bags to create
sim_dir        = 'results/example_parallelbeam_2d/' # simulation directory
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Step 2: Specify Scanner Model using scanner_template.py

scanner_mdl = ScannerTemplate(
                geometry='parallel',
                scan='circular',
                machine_dict=default_scanner_parallel.machine_geometry,
                recon='fbp',
                recon_dict=default_scanner_parallel.recon_params,
                pscale=1.0
                )

scanner_mdl.set_recon_geometry()
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Step 3: Specify X-ray Source Model

# The X-ray Source Model is specified by a dictionary with the following
# key-value pairs:
# num_spectra  - No of X-ray sources/spectra
# kVp          - peak kV voltage for all the X-ray source(s)
# spectra      - file paths for the each of the X-ray spectra.
#                The spectrum files are .txt files containing a N x 2
#                array with the keV values in the first column and
#                normalized photon distribution in the 2nd column.
#                See /include/spectra/ for examples to create your own
#                spectrum file.
# dosage       - dosage count for each of the sources

xray_source_specs = dict(num_spectra=1,
                         kVp=130,
                         spectra=[os.path.join(SPECTRA_DIR,
                                               'example_spectrum_130kV.txt')
                                  ],
    dosage=[1.8e5]
)
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Step 4: Specify the arguments the BaggageCreator2D() Arguments - these
# arguments decide the nature of objects spawned in the simulated bags.

# The list contains the list of materials that will be assigned to the
# objects in the bag - the material assignment is random but liquids need
# to be specified separately if liquid filled containers are to be spawned.

mlist    = ['ethanol',                                       # organic
            'Al', 'Ti', 'Fe',                                # metals
            'bakelite', 'pyrex','acrylic', 'Si',             # glass/
                                                             # ceramics
            'polyethylene',  'pvc', 'polystyrene', 'acetal', # plastics
            'neoprene',                                      # rubber
            'nylon6', 'teflon',                              # cloth
            ]
lqd_list = ['water', 'H2O2']                                 # liquids

# material selection probabilities
material_pdf = [0.3] + [0.05/3]*3 + [0.65/11]*11
liquid_pdf = [1/2., 1/2.]

# using custom shapes other than fixed geometries
custom_objects = [os.path.join(CUSTOM_SHAPES_DIR, s)
                  for s in os.listdir(CUSTOM_SHAPES_DIR)]

bag_creator_args = dict(
    # list of materials/liquids to simulate -----------------------------------
    material_list=mlist,
    liquid_list=lqd_list,
    # material selection probabilities - specify for each material ------------
    material_pdf=material_pdf,
    liquid_pdf=liquid_pdf,
    # params for deformable sheets/liquid-filled containers -------------------
    spawn_sheets=True,
    spawn_liquids=True,
    sheet_prob=0.2,       # probability of spawning a deformable sheet
    lqd_prob=0.3,         # probability of spawning a liquid-filled container
    sheet_dim_list=range(2, 7),  # range of sheet thicknesses
    # -------------------------------------------------------------------------
    # object shape specifications
    dim_range=(20,70),                   # min-max dims of simulated object
    number_of_objects=range(30, 40),     # number of objects in each bag
    custom_objects=custom_objects, # if custom objects are to be specified
    custom_obj_prob=0.3,           # probability of spawning a custom shape
    # -------------------------------------------------------------------------
    # specifications for metals / target objects
    metal_dict={'metal_amt':  8e2, 'metal_size': (3,5)},
    target_dict={'num_range': (1,3), 'is_liquid': False}
    # -------------------------------------------------------------------------
)
# -----------------------------------------------------------------------------
# Step 4 Specify the Dual Energy Decomposition Method

# not needed to specify for single energy setup

# -----------------------------------------------------------------------------
# Step 5: Forward Model Args

fwd_mdl_args = dict(add_poisson_noise=True,
                    add_system_noise=True,
                    system_gain=0.025949
                   )

# -----------------------------------------------------------------------------
# params to feed to the debisim pipeline
params = dict()

params['num_bags']          = bags_to_create
params['sim_dir']           = sim_dir
params['scanner']           = scanner_mdl
params['xray_src_mdl']      = xray_source_specs
params['bag_creator_args']  = bag_creator_args
params['fwd_mdl_args']      = fwd_mdl_args
params['save_sino']         = False
params['basis_fn']          = None
params['decomposer_args']   = None
params['recon_args']        = None
params['images_to_save']    = ['gt']
params['decomposer']        = 'none'
params['slicewise']         = True # set if creating 2D cross-sections instead
                                   # of 3D bags
# -------------------------------------------------------------------------------
