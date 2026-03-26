import math

def merge_chunks(chunks, n =5):
    new_chunks = []
    num_chunks = len(chunks)
    num_groups = math.ceil(num_chunks/n)
    
    for i in range(num_groups):
        start_idx = i*n
        end_idx = min((i+1)*n, num_chunks)
        group = chunks[start_idx:end_idx]
        
        new_chunks.append({
            "video_number": group[0]["video_number"],
            "title": group[0]["title"],
            "start": group[0]["start"],
            "end": group[-1]["end"],
            "text": " ".join(c["text"] for c in group)  
        })
    return new_chunks




