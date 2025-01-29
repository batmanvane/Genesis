import genesis as gs

#gs.init(backend=gs.metal)

gs.init(
    seed                = None,
    precision           = '32',
    debug               = False,
    eps                 = 1e-12,
    logging_level       = None,
    backend             = gs.metal,
    theme               = 'dark',
    logger_verbose_time = False
)

# scene = gs.Scene()

scene = gs.Scene(
    show_viewer    = True,
    viewer_options = gs.options.ViewerOptions(
        res           = (1280, 960),
        camera_pos    = (3.5, 0.0, 2.5),
        camera_lookat = (0.0, 0.0, 0.5),
        camera_fov    = 40,
        max_FPS       = 60,
    ),
    vis_options = gs.options.VisOptions(
        show_world_frame = True, # visualize the coordinate frame of `world` at its origin
        world_frame_size = 1.0, # length of the world frame in meter
        show_link_frame  = False, # do not visualize coordinate frames of entity links
        show_cameras     = False, # do not visualize mesh and frustum of the cameras added
        plane_reflection = True, # turn on plane reflection
        ambient_light    = (0.1, 0.1, 0.1), # ambient light setting
    ),
    renderer = gs.renderers.Rasterizer(), # using rasterizer for camera rendering
    sim_options=gs.options.SimOptions(
        dt=0.01,
        gravity=(0.0, 0.0, -9.81),
    ),
)

plane = scene.add_entity(
    gs.morphs.Plane(),
)
franka = scene.add_entity(
    # gs.morphs.URDF(
    #     file='urdf/panda_bullet/panda.urdf',
    #     fixed=True,
    # ),
    gs.morphs.MJCF(file="xml/franka_emika_panda/panda.xml"),
)


scene.build()

def run_sim(scene):
    for i in range(100):
        scene.step()

# You need to run simulation in a separate thread on MacOS
gs.tools.run_in_another_thread(fn=run_sim, args=(scene,))
# This must be called from the main thread after starting the thread
scene.viewer.start()
