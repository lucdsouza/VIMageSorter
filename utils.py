def format_bytes(size):
    if size < 1024:
        return f"{size} B"
        
    elif size < 1024**2:
        return f"{size/1024:.1f} KB"

    elif size < 1024**3:
        return f"{size/(1024**2):.1f} MB"

    elif size < 1024**4:
        return f"{size/(1024**3):.1f} GB"
    
    return f"{size/(1024**4):.1f} TB"

