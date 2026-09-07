import pymupdf

def verify_signature_and_stamp(pdf_bytes: bytes) -> dict:
    """
    Lightweight CV check for signatures and stamps.
    Checks the bottom 30% of each page for:
    1. Embedded images (digital signatures/scans)
    2. Blue/Violet pixel density (rubber stamps / blue ink)
    """
    try:
        doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
        page_results = []
        all_valid = True
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # 1. Check for embedded images (often digital signatures/stamps)
            images = page.get_images(full=True)
            has_image = len(images) > 0
            
            # 2. Check for Blue/Violet pixels in the bottom 70% of the page
            # (Because short documents have blank white space in the bottom 30%)
            rect = page.rect
            bottom_rect = pymupdf.Rect(0, rect.height * 0.3, rect.width, rect.height)
            pix = page.get_pixmap(clip=bottom_rect)
            
            samples = pix.samples
            n = pix.n # 3 for RGB, 4 for RGBA
            blue_pixel_count = 0
            
            # Fast heuristic: sample every 10th pixel to detect blue/violet
            # Blue/Violet typically means B > R + 20 and B > G + 20 and B > 80
            for i in range(0, len(samples), n * 10):
                r = samples[i]
                g = samples[i+1]
                b = samples[i+2]
                if b > r + 20 and b > g + 20 and b > 80:
                    blue_pixel_count += 1
                    
            # Arbitrary threshold for blue pixel cluster
            has_blue_ink = blue_pixel_count > 10
            
            is_valid = has_image or has_blue_ink
            if not is_valid:
                all_valid = False
                
            page_results.append({
                "page": page_num + 1,
                "has_image_signature": has_image,
                "has_blue_ink": has_blue_ink,
                "valid": is_valid
            })
            
        return {
            "is_signed_and_stamped": all_valid,
            "pages": page_results
        }
    except Exception as e:
        return {"is_signed_and_stamped": False, "error": str(e)}
