from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.decorators import authentication_classes,permission_classes
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import filters
from rest_framework import generics
from datetime import date, timedelta, timezone

from .serializers import cuboidSerializer
from .models import cuboid

@api_view(['GET'])
def apiOverview(request):
	api_urls = {
		'ListAll':'/cuboid-list-all/',
		'List':'/cuboid-list/',
		'Create':'/cuboid-create/',
		'Update':'/cuboid-update/<str:pk>/',
		'Delete':'/cuboid-delete/<str:pk>/',
		}
	return Response(api_urls)


class cuboidALListView(generics.ListAPIView):
	queryset = cuboid.objects.all()
	serializer_class = cuboidSerializer
	authentication_classes = (SessionAuthentication,BasicAuthentication)
	permission_classes = [IsAuthenticated]
	filter_backends = [filters.OrderingFilter,filters.SearchFilter]
	search_fields =['=created_by__username','created_at']
	ordering_fields = ['length', 'breadth','height',"area","volume"]

class cuboidListView(generics.ListAPIView):
	serializer_class = cuboidSerializer
	authentication_classes = (SessionAuthentication,BasicAuthentication)
	permission_classes = [IsAuthenticated,IsAdminUser]
	filter_backends = [filters.OrderingFilter,filters.SearchFilter]
	ordering_fields = ['length', 'breadth','height',"area","volume"]
	def get_queryset(self):
		username=self.request.user.username
		if username:
			return cuboid.objects.filter(created_by=username)
	



@api_view(['GET','POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated,IsAdminUser])
def cuboidCreate(request):
	try:
		if request.method=="POST":
			l,b,h=request.data["length"],request.data["breadth"],request.data["height"]
			l,b,h=int(l),int(b),int(h)
			created_by=request.user.username
			area=2*l*b+2*b*h+2*l*h
			volume=l*b*h
			a_area=[i.area for i in cuboid.objects.all()]
			a_volume=[i.volume for i in cuboid.objects.filter(created_by=request.user.username)]
			avg_area=(sum(a_area)+area)/(len(a_area)+1)
			avg_volume=(sum(a_volume)+volume)/(len(a_volume)+1)
			if avg_area<=100 and avg_volume<=1000:
				enddate= date.today()+timedelta(days=1)
				startdate = enddate - timedelta(days=8)
				count_week=cuboid.objects.filter(created_at__range=[startdate, enddate]).count()
				if count_week<=100:
					count_week_user=cuboid.objects.filter(created_at__range=[startdate, enddate],created_by=request.user).count()
					if count_week_user<=50:
						data={
							"length":l,
							"breadth":b,
							"height":h,
							"area":area,
							"volume":volume,
							"created_by":created_by
						}
						serializer = cuboidSerializer(data=data)
						if serializer.is_valid():
							serializer.save()
							return Response(serializer.data)
						return Response("Boxes added by the user in this week exceed the limit")
				return Response("Boxes added in this week exceed the limit")
			return Response("average of area or volume of cuboid  is exceeded")
		elif request.method=="GET":
			data_req = {
					'length':"must required format integer",
					'breadth':"must required format integer",
					'height':"must required format integer"
			}
		return Response(data_req)
	except :
		return Response({
					'length':"must required format integer",
					'breadth':"must required format integer",
					'height':"must required format integer"
			})




@api_view(['GET','POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def cuboidUpdate(request, pk):
	try:
		task = cuboid.objects.get(id=pk)
		if request.method=="POST":
			l=request.data.get("length") if request.data.get("length",None) else  task.length
			b=request.data.get("breadth")  if request.data.get("breadth",None) else task.breadth
			h= request.data.get("height") if request.data.get("height",None) else task.height
			area=2*l*b+2*b*h+2*l*h
			volume=l*b*h
			a_area=[i.area for i in cuboid.objects.all()]
			a_volume=[i.volume for i in cuboid.objects.filter(created_by=request.user.username)]
			avg_area=(sum(a_area)+area)/(len(a_area)+1)
			avg_volume=(sum(a_volume)+volume)/(len(a_volume)+1)
			if avg_area<=100 and avg_volume<=1000:
				data={
					"length":l,
					"breadth":b,
					"height":h,
					"area":area,
					"volume":volume,
					'created_by':task.created_by
				}
				serializer = cuboidSerializer(instance=task, data=data)
				print(serializer.is_valid)
				if serializer.is_valid():
					serializer.save()
					return Response(serializer.data)

			return Response("you can't change the size of the cuboid because it exceeding it's limits.")

		elif request.method=="GET":
			return Response({
					'id':task.id,
					'length':task.length,
					'breadth':task.breadth,
					'height':task.height,
					'area':task.area,
					'volume':task.volume,
					'created_by':task.created_by.username,
					'created_at':task.created_at
				})
	except :
		return Response('something went wrong please try again after some time',status=400)


@api_view(['GET','DELETE'])
@authentication_classes([SessionAuthentication,BasicAuthentication])
@permission_classes([IsAuthenticated,IsAdminUser])
def cuboidDelete(request, pk):
	try:
		task = cuboid.objects.get(id=pk)
		if request.method=="DELETE":
			task.delete()
			return Response('Item succsesfully delete!')
		elif request.method=="GET":
			return Response({
					'id':task.id,
					'length':task.length,
					'breadth':task.breadth,
					'height':task.height,
					'area':task.area,
					'volume':task.volume,
					'created_by':task.created_by.username,
					'created_at':task.created_at	
				})
	except :
		return Response('something went wrong please try again after some time',status=400)
