from app import create_app
try:
    app = create_app()
    print("SUCCESS")
except Exception as e:
    print("ERROR:", e)
    import traceback
    traceback.print_exc()