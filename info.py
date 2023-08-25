class NovelInfo:
    def __init__(self, platform, title, info, agegrade, category, view, id, content_type, free_type, new_status, thumbnail):
        self.platform = platform
        self.title = title
        self.info = info
        self.agegrade = agegrade
        self.category = category
        self.view = view
        self.id = id
        self.content_type = content_type
        self.free_type = free_type
        self.new_status = new_status
        self.thumbnail = thumbnail

    def __str__(self):
        return f"platform: {self.platform}, title: {self.title}, info: {self.info}, grade: {self.agegrade}, category: {self.category}, view: {self.view}, id: {self.id}, content_type: {self.content_type}, free_type: {self.free_type}, new_status: {self.new_status}, thumbnail: {self.thumbnail}"

    def to_dict(self):
        return {
            "platform": self.platform,
            "title": self.title,
            "info": self.info,
            "agegrade": self.agegrade,
            "category": self.category,
            "view": self.view,
            "id": self.id,
            "content_type": self.content_type,
            "free_type": self.free_type,
            "new_status": self.new_status,
            "thumbnail": self.thumbnail
        }

def set_novel_info(platform, title, info, agegrade, category, view, id, content_type, free_type, new_status, thumbnail):
    print("-" * 100)
    print(f"platform: {platform}")
    print(f"title: {title}")
    print(f"info: {info}")
    print(f"grade: {agegrade}")
    print(f"category: {category}")
    print(f"view: {view}")
    print(f"id: {id}")
    print(f"content_type: {content_type}")
    print(f"free_type: {free_type}")
    print(f"new_status: {new_status}")
    print(f"thumbnail: {thumbnail}")
    print("-" * 100)
    return NovelInfo(platform, title, info, agegrade, category, view, id, content_type, free_type, new_status, thumbnail)
