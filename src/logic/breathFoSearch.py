from config import max_depth

Neghibor = [(-1,0),(1,0),(0,-1),(0,1)]  

def start_search_shortes(grid):
    fund = False
    i = 1 
    limet = max_depth
    path = []
    while not fund and i < limet:
        visited = set()
        moves, dirction = grid.muligMoves([0,0])
        for move, dirction in zip(moves,dirction):
            # print(move,dirction)
            path.append(move)
            grid.move(move)
            # visited.append(grid.return_gride_state())
            if search(0,i,grid, move, dirction, path, visited):
                fund = True
                grid.undoMove()
                break
            grid.undoMove()
            path.pop()
        i+=1
        print(i)
    # print(path)
    return path

def start_search(grid):
    path = []
    visited = set()
    moves, dirction = grid.muligMoves([0,0])
    for move, dirction in zip(moves,dirction):
        # print(move,dirction)
        path.append(move)
        grid.move(move)
        # visited.append(grid.return_gride_state())
        if search(0,max_depth,grid, move, dirction, path, visited):
            fund = True
            grid.undoMove()
            break
        grid.undoMove()
        path.pop()

    # print(path)
    return path
    


def search(depth, max_depth, grid, curentmove,premove,currentPath:list,visited):
    # print(depth)
    if depth >= max_depth:
        # print("Depth")
        return False
    
    state = grid.return_gride_state()
    if state in visited:
        # print("besøkt")

        return False
    
    visited.add(state)
    
    if grid.win():
        # print("dunnet")
        return True
    
    moves, dirction = grid.muligMoves(premove)
    if len(moves) == 0:
        return False
    
    # print(f"{curentmove}:: {moves} ")
    for move, dirction in zip(moves,dirction):
        # print("nest move")
        grid.move(move)
        grid.preMove.append([])
        grid.preMove[-1].append(move)
        currentPath.append(move)
        if search(depth+1, max_depth, grid ,move,dirction,currentPath,visited):
            grid.undoMove()
            return True
        grid.undoMove()
        currentPath.pop()
        
    visited.remove(state)
    return False