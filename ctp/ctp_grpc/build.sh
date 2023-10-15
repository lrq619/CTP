python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ctp.proto
file="ctp_pb2_grpc.py"
cp "$file" "${file}.bak"

awk 'NR==4{print $0; print "import sys\nimport os\n\nsys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))"} NR!=4' "${file}.bak" > "$file"
rm "${file}.bak"