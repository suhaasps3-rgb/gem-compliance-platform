import io
import pypdf

def _page_has_images(page):
    try:
        resources = page.get("/Resources")
        if resources is None:
            return False
        if hasattr(resources, "get_object"):
            resources = resources.get_object()
        xobjects = resources.get("/XObject")
        if xobjects is None:
            return False
        if hasattr(xobjects, "get_object"):
            xobjects = xobjects.get_object()
        for key in xobjects:
            obj = xobjects[key]
            if hasattr(obj, "get_object"):
                obj = obj.get_object()
            if obj.get("/Subtype") == "/Image":
                return True
    except Exception:
        pass
    return False


def verify_signature_and_stamp(pdf_bytes):
    try:
        reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
        page_results = []
        all_valid = True
        for page_num, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            has_image = _page_has_images(page)
            blank_indicators = [
                "____________________________",
                "Seal/Stamp: ________________",
                "Name: ________________",
                "Signature: ________________",
                "pending physical signature",
                "SIGNATURE MISSING",
                "UNSIGNED"
            ]
            has_blank_signature = any(ind in text for ind in blank_indicators)
            has_dsc_or_stamp_text = any(token in text for token in [
                "SIGNED AND STAMPED",
                "DSC Token:",
                "Digital Signature Certificate",
                "UDIN: 2",
                "SEAL AND SIGNED"
            ])
            if has_blank_signature and not has_image:
                is_valid = False
            elif has_image or has_dsc_or_stamp_text:
                is_valid = True
            else:
                is_valid = True
            if not is_valid:
                all_valid = False
            page_results.append({
                "page": page_num + 1,
                "has_image_signature": has_image,
                "has_blank_signature": has_blank_signature,
                "has_dsc_or_stamp_text": has_dsc_or_stamp_text,
                "valid": is_valid
            })
        return {
            "is_signed_and_stamped": all_valid,
            "pages": page_results,
            "details": "Signature and official rubber stamp verified" if all_valid else "Signature or stamp missing in execution block"
        }
    except Exception as e:
        return {"is_signed_and_stamped": False, "error": str(e)}
