from flask import Blueprint, render_template,request
import requests
components = Blueprint("components", __name__)

    #    task = request.form.to_dict(flat=True)
    #     # Create a new resource
    #     print(request.url_root +'/api주소')
    #     response = requests.post(request.url_root + '/api주소', json = task)
    #     print('response from server:',response.text)
    #     dictFromServer = response.json()        
    #     print(task, dictFromServer)
headers = {'Cookie': 'Toy Movie=.eJyrVsrJLC6Jz8svV7Iy0IFwilKTU_NKEPySotS8FDC3KLUsM7U8viC_oDQnsUjJyhAuBNODEIHpqgUAwbUiog.YxpgHg.h2D89E2huUu1yIOr9UA8T2ZFXjU'}
moview = {'movies': [{'actor': '톰 크루즈|제니퍼 코넬리|마일즈 텔러', 'code': 81888, 'director': '조셉 코신스키', 'image': 'https://movie-phinf.pstatic.net/20220509_176/1652081912471yhg3N_JPEG/movie_image.jpg', 'naverRating': '9.76', 'pubDate': '2022.06.22', 'title': '탑건: 매버릭'}, {'actor': '신시아|박은빈|서은수|진구|성유빈|조민수', 'code': 196367, 'director': '박훈정', 'image': 'https://movie-phinf.pstatic.net/20220615_63/1655270906406BGdFF_JPEG/movie_image.jpg', 'naverRating': '6.59', 'pubDate': '2022.06.15', 'title': '마녀(魔女) Part2. The Other One'}, {'actor': '송강호|강동원|배두나|아이유|이주영', 'code': 196854, 'director': '고레에다 히로카즈', 'image': 'https://movie-phinf.pstatic.net/20220511_189/1652251073330PXNoG_JPEG/movie_image.jpg', 'naverRating': '5.53', 'pubDate': '2022.06.08', 'title': '브로커'}, {'actor': '마동석|손석구|최귀화', 'code': 192608, 'director': '이상용', 'image': 'https://movie-phinf.pstatic.net/20220516_144/1652665409592Chvey_JPEG/movie_image.jpg', 'naverRating': '9.33', 'pubDate': '2022.05.18', 'title': '범죄도시2'}]}
@components.route("/reviewcard")
def review_card():
   return render_template("components/review_card.html",movies=[1,2])

@components.route("/postercard-v")
def poster_card_v():
   print(request.url_root +'now?dir=left')
   response = requests.get(request.url_root + 'now?dir=left',headers=headers)
   print(response.json())
   movies = response.json()["movies"]
#    dictFromServer = response.json()
#    print( dictFromServer)
   return render_template("components/poster_card.html",movies=movies,direction="vertical")

@components.route("/postercard-h")
def poster_card_h():
   return render_template("components/poster_card.html",movies=[1,2,3,4],direction="horizontal")

@components.route("/signup")
def sign_up():
   tag_id = request.args.get("tagid")
   return render_template("components/sign_up.html",tag_to_empty=tag_id)

@components.route("/signin")
def sign_in():
   tag_id = request.args.get("tagid")
   return render_template("components/sign_in.html",tag_to_empty=tag_id)

@components.route("/moviesearch")
def create():
   cover= request.args.get("cover")
   tag_id = request.args.get("tagId")
   return render_template("components/movieSearch.html",is_modal_covered=cover,tag_to_empty=tag_id)

@components.route("/upsert")
def upsert():
   return render_template("components/review_upsert.html",movie_title="tenet create",title="Make Review",make_edit="make") 

@components.route("/popup-upsertied")
def popup_upsertied():
   return render_template("components/popup.html",message="제출되었습니다")

@components.route("/view-review")
def view_review():
   tag_to_empty = request.args.get("tagId")
   return render_template("components/review.html",tag_to_empty=tag_to_empty)

@components.route("/edit")
def edit():
   print("edit")
   return render_template("components/review_upsert.html",movie_title="tenet edit",title="Edit Review",make_edit="edit")