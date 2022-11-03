try:
	import main
except Exception as error:
	print(error)
except KeyboardInterrupt:
	print("KeyboardInterrupt")