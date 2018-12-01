from flask import Flask, request
from flask_restful import Resource, Api
from flask_restful import reqparse
import pysql
import werkzeug, os
import pano
import cv2
from BookSegmentation import *
from RecognitionText import *
#from aidDef import *
from GradCrawler import *
import pymysql

UPLOAD_FOLDER = 'static/images'

app = Flask(__name__)
api = Api(app)

class Todo(Resource):
	def post(self):
		try:
			parser = reqparse.RequestParser()
			parser.add_argument('img1',type=werkzeug.datastructures.FileStorage,location='files')
			#parser.add_argument('img2',type=werkzeug.datastructures.FileStorage,location='files')
			#parser.add_argument('img3',type=werkzeug.datastructures.FileStorage,location='files')
			
			args = parser.parse_args()
			
			if args['img1'] == "":
				return {'error':'not img'}
			#store
			_img1 = args['img1']
			
			if _img1:
				_img1.save(os.path.join(UPLOAD_FOLDER,'img1.jpg'))

			print("step0 : store img")
			##stiching
			#print("Stitch start")
			#path = "txtlists/files1.txt"
			#s = pano.Stitch(path)
			#s.leftshift()
			## s.showImage('left')
			#s.rightshift()
			#cv2.imwrite("C:/Users/err20/source/repos/Python_Study/Python_Study/static/result/test.jpg", s.leftImage)
			#print("image written")
			#cv2.destroyAllWindows()
			#img cut
			#print('cut start')
			BookClass = BookSpineDetector("/home/grad/flaskapp/app/static/images/img1.jpg")
			#print('~ing')
			lst = BookClass.get_book_spine()

			print("step0 : cut img")
			##goolge
			results = recognition_book(lst, BookClass.img)

			print("step0 : google Api")
			#C
			
			#dp = [[0]*1000 for i in range(1000)]

			#print(results)
			conn = pymysql.connect(
				user = 'grad',
				passwd = 'snrn132@',
				host = '49.236.137.29',
				port=3306,
				db='grad',
				charset='utf8')
			#print("start")
			print("step0 : connect DB")
			for result in results:
				incompletionName = result.split('\n')
				#print(completeName(incompletionName[0]))
				good = completeName(incompletionName[0])
				if good[0] != -1:
					print("step7 : result : ",good)
					pysql.insertSql(good,conn)
			print('success All!!')
			#items = same(result)

			return {'status':'success'}
		except Exception as e:
			return {'error':str(e)}

api.add_resource(Todo, '/sendimg')

if __name__ == '__main__':
    app.run(host='0.0.0.0')