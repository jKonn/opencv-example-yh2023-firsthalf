import cv2
import pafy

#pip install pafy
#pip install youtube-dl

# pafy 오류 수정 참조:
# https://syerco0.com/37

# 해당경로안 youtube.py 파일을 찾아서 연다
# ./venv/lib/python3.8/site-packages/youtube_dl/extractor
# 검색 'uploader_id': self. 후 해당 줄의 내용을 변경
# 변경될 내용 => 'uploader_id': self._search_regex(r'/(?:channel/|user/|@)([^/?&#]+)', owner_profile_url, 'uploader id', default=None),
# 정규식에 @가 추가됨

# key 인덱스 에러 수정 ('like_count', 'dislike_count')
# backend_youtube_dl.py 파일을 찾아서 연다
# ./venv/lib/python3.8/site-packages/pafy/backend_youtube_dl.py
# 검색 => self._ydl_info['like_count'] | self._ydl_info['dislike_count']
# 변경 => self._ydl_info.get('like_count',0) | self._ydl_info.get('like_count',0)

url = "https://www.youtube.com/watch?v=QyBdhdz7XM4"
# url = "https://www.youtube.com/watch?v=Yb4saNDmddU"

video = pafy.new(url)
# best = video.getbest()
best = video.getbest(preftype="mp4")

# 버퍼 열림 (캡쳐 시작)
# cap = cv2.VideoCapture(best.url)
cap = cv2.VideoCapture(best.url)

# 파일이 정상적으로 열렸는지 확인
if cap.isOpened():
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow(best.url, frame)
        if cv2.waitKey(25) >= 0:
            break

#버퍼 닫음 (캡쳐 종료)
cap.release()
cv2.destroyAllWindows()
