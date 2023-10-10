class Run:
    def __enter__(self):
        print("Enter run")
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Exit run")
    pass