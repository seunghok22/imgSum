from PIL import Image
import os

def merge_file_lists(fixed_list, moving_list):
    merge_list = []
    try:
        idx = fixed_list.index('')
        for moving_set in moving_list:
            merged = fixed_list[:idx] + moving_set + fixed_list[idx+1:]
            merge_list.append(merged)
    except ValueError:
        for moving_set in moving_list:
            merged = fixed_list + moving_set
            merge_list.append(merged)
    return merge_list

def create_images_from_merge_list(merge_list, output_dir, width=None):
    """
    merge_list: 2차원 리스트, 각 내부 리스트는 합칠 이미지 파일명 리스트
    output_dir: 합쳐진 이미지를 저장할 폴더 경로 (사용자 입력)
    width: 최종 이미지의 고정 가로 길이 (None이면 가장 큰 이미지의 width)
    결과 이미지는 output_dir에 세로로 합쳐 저장, 각 이미지는 가로 중앙에 정렬
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i, file_list in enumerate(merge_list):
        images = []
        for fname in file_list:
            img_path = os.path.join(os.getcwd(), fname)
            if os.path.exists(img_path):
                images.append(Image.open(img_path))
            else:
                print(f"파일 없음: {img_path}")

        if not images:
            print(f"{i}번째 이미지 리스트에 합칠 이미지가 없습니다.")
            continue

        # 고정 width가 없으면 가장 큰 이미지의 width 사용
        max_width = width if width is not None else max(img.size[0] for img in images)
        total_height = sum(img.size[1] for img in images)
        new_im = Image.new('RGBA', (max_width, total_height), (255, 255, 255, 0))
        y_offset = 0
        for im in images:
            x_offset = (max_width - im.size[0]) // 2  # 가운데 정렬
            new_im.paste(im, (x_offset, y_offset))
            y_offset += im.size[1]

        output_path = os.path.join(output_dir, f'merged_image_{i+1}.png')
        new_im.save(output_path)
        print(f"{i+1}번째 합쳐진 이미지가 저장되었습니다: {output_path}")