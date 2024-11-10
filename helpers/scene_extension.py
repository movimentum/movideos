class SceneExtension:
    video_orientation = 'portrait'
    render_all_sections = False
    
    CONFIG = None
    
    @classmethod
    def skip(cls, should_skip_locally):
        return should_skip_locally and not cls.render_all_sections
        
