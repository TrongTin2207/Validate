import networkx as nx

def validate_solution(solutionFile, SFCGraphs, PHYGraph):
    # Đọc file kết quả và lấy giá trị các biến
    # Giả sử file kết quả chứa các giá trị biến theo định dạng JSON
    import json
    with open(solutionFile, 'r') as file:
        solution = json.load(file)
    
    # Lấy giá trị các biến từ file kết quả
    phiLink = solution['phiLink']
    phiNode = solution['phiNode']
    phiSFC = solution['phiSFC']
    
    # Kiểm tra các giá trị đọc được có thoả mãn 5 constrains hay không
    # Constraint 1: Tất cả các liên kết VW của SFC phải được đặt tại một liên kết IJ
    for sfc in phiLink.keys():
        for vw, ij in phiLink[sfc].items():
            if ij not in PHYGraph.edges:
                return False
    
    # Constraint 2: Tất cả các VNF của SFC phải được đặt tại một nút I
    for sfc in phiNode.keys():
        for v, i in phiNode[sfc].items():
            if i not in PHYGraph.nodes:
                return False
    
    # Constraint 3: Mỗi SFC phải được map vào mạng vật lý
    for sfc in phiSFC.keys():
        if phiSFC[sfc] not in PHYGraph.nodes:
            return False
    
    # Constraint 4: Mỗi nút I chỉ được đặt một VNF của cùng một SFC
    for sfc in phiNode.keys():
        used_nodes = set()
        for v, i in phiNode[sfc].items():
            if i in used_nodes:
                return False
            used_nodes.add(i)
    
    # Constraint 5: Mỗi liên kết IJ chỉ được đặt một liên kết VW của cùng một SFC
    for sfc in phiLink.keys():
        used_edges = set()
        for vw, ij in phiLink[sfc].items():
            if ij in used_edges:
                return False
            used_edges.add(ij)
    
    # Nếu tất cả các constrains đều thoả mãn, trả về True
    return True