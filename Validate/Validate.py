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
    
    # Kiểm tra ràng buộc 1: Tổng tài nguyên yêu cầu tại một nút vật lí không vượt quá tổng tài nguyên có sẵn tại nút vật lí đó
    for sfc in phiNode.keys():
        for v, i in phiNode[sfc].items():
            required_capacity = SFCGraphs[sfc].nodes[v]['capacity']
            available_capacity = PHYGraph.nodes[i]['capacity']
            if required_capacity > available_capacity:
                return False
    
    # Kiểm tra ràng buộc 2: Tổng tài nguyên yêu cầu tại một liên kết vật lí không vượt quá tổng tài nguyên mà nút vật lí đó có
    for sfc in phiLink.keys():
        for vw, ij in phiLink[sfc].items():
            required_weight = SFCGraphs[sfc].edges[vw]['weight']
            available_weight = PHYGraph.edges[ij]['weight']
            if required_weight > available_weight:
                return False
    
    # Kiểm tra ràng buộc 3: Mỗi nút vật lí chỉ chứa tối đa một VNF của một SFC
    for sfc in phiNode.keys():
        used_nodes = set()
        for v, i in phiNode[sfc].items():
            if i in used_nodes:
                return False
            used_nodes.add(i)
    
    # Kiểm tra ràng buộc 4: Mỗi VNF của mỗi SFC đều được chứa trong một nút vật lí
    for sfc in phiNode.keys():
        for v in SFCGraphs[sfc].nodes:
            found = False
            for i in phiNode[sfc].values():
                if v in phiNode[sfc] and phiNode[sfc][v] == i:
                    found = True
                    break
            if not found:
                return False
    
    # Kiểm tra ràng buộc 5: Mọi SFC đều được bảo toàn về chiều dịch vụ
    for sfc in phiSFC.keys():
        for neighbor in SFCGraphs[sfc].predecessors(sfc):
            if neighbor not in phiSFC.keys():
                return False
    
    # Nếu tất cả các ràng buộc đều thoả mãn, trả về True
    return True
