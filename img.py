from PIL import Image

def save_combined_images_optimized(static_images, flex_images, position, num):
    """
    static_images: [(PIL.Image, filename), ...]
    flex_images: [(PIL.Image, filename), ...]
    position: int
    num: List[int]
    """
    if not static_images:
        print("static_images가 비어있습니다.")
        return
    # 첫 이미지의 width 사용 (모두 같다고 가정)
    max_width = static_images[0][0].width
    total_height = sum(img.height for img, _ in static_images)
    used_img_idx = 0

    for i in range(len(num)):
        start_idx = used_img_idx
        used_img_idx += num[i]
        temp_height = total_height + sum(img.height for img, _ in flex_images[start_idx:used_img_idx])
        new_img = Image.new('RGB', (max_width, temp_height), (255, 255, 255))

        y_offset = 0
        for idx, (img, _) in enumerate(static_images):
            if idx == position:
                for flex_img, _ in flex_images[start_idx:used_img_idx]:
                    # 가로길이 같으므로 임시 이미지 없이 바로 붙이기
                    new_img.paste(flex_img, (0, y_offset))
                    y_offset += flex_img.height
            new_img.paste(img, (0, y_offset))
            y_offset += img.height

        try:
            filename = f"output_{i+1}.png"
            new_img.save(filename)
            print(f"{filename} 저장 완료")
        except Exception as e:
            print(f"이미지 저장 중 오류 발생: {e}")