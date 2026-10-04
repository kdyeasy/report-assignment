import time

def get_matrix():
    n = int(input("행렬 크기 입력: "))
    print(f"{n} x {n} 행렬을 입력하세요")
    
    m = []
    for _ in range(n):
        temp_input = input().split()
        row = []
        for x in temp_input:
            row.append(float(x))
        m.append(row)
        
    return m

def get_minor(mat, r, c):
    sub_m = []
    size = len(mat)
    for i in range(size):
        if i == r:
            continue
        new_row = []
        for j in range(size):
            if j == c:
                continue
            new_row.append(mat[i][j])
        sub_m.append(new_row)
    return sub_m

def get_det(mat):
    size = len(mat)
    if size == 1:
        return mat[0][0]
    if size == 2:
        return mat[0][0] * mat[1][1] - mat[0][1] * mat[1][0]
    
    total = 0
    for j in range(size):
        if j % 2 == 0:
            sik = 1
        else:
            sik = -1
            
        sub = get_minor(mat, 0, j)
        total += sik * mat[0][j] * get_det(sub)
        
    return total

def m_inv1(mat):
    d = get_det(mat)
    
    if abs(d) < 1e-9:
        return None 
        
    size = len(mat)
    if size == 1:
        return [[1 / mat[0][0]]]
        
    cof_m = []
    for i in range(size):
        r_data = []
        for j in range(size):
            if (i + j) % 2 == 0:
                sik = 1
            else:
                sik = -1
            sub = get_minor(mat, i, j)
            r_data.append(sik * get_det(sub))
        cof_m.append(r_data)
        
    result_m = []
    for i in range(size):
        r_data = []
        for j in range(size):
            v = cof_m[j][i] / d
            r_data.append(v)
        result_m.append(r_data)
        
    return result_m

def m_inv2(mat):
    size = len(mat)
    a_mat = []
    
    for i in range(size):
        r_data = []
        for j in range(size):
            r_data.append(mat[i][j])
        for j in range(size):
            if i == j:
                r_data.append(1.0)
            else:
                r_data.append(0.0)
        a_mat.append(r_data)
        
    for i in range(size):
        if abs(a_mat[i][i]) < 1e-9:
            switched = False
            for k in range(i + 1, size):
                if abs(a_mat[k][i]) > 1e-9:
                    t = a_mat[i]
                    a_mat[i] = a_mat[k]
                    a_mat[k] = t
                    switched = True
                    break
            if not switched:
                return None
                
        p = a_mat[i][i]
        for j in range(size * 2):
            a_mat[i][j] = a_mat[i][j] / p
            
        for k in range(size):
            if k != i:
                f = a_mat[k][i]
                for j in range(size * 2):
                    a_mat[k][j] -= f * a_mat[i][j]
                    
    result_m = []
    for i in range(size):
        r_data = []
        for j in range(size, size * 2):
            r_data.append(a_mat[i][j])
        result_m.append(r_data)
        
    return result_m

def print_matrix(mat):
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            val = mat[i][j]
            if abs(val - round(val)) < 1e-4:
                print(f"{int(round(val))}", end="\t")
            else:
                print(f"{round(val, 4)}", end="\t")
        print() 

def check_same(m1, m2):
    if m1 is None or m2 is None:
        return m1 == m2
            
    size = len(m1)
    for i in range(size):
        for j in range(size):
            if abs(m1[i][j] - m2[i][j]) > 1e-3:
                return False
    return True


input_data = get_matrix()

print("\n[방법1 : 행렬식 이용]")
t_start1 = time.time()

get_d = get_det(input_data)
if abs(get_d - round(get_d)) < 1e-4:
    print(f" -> 행렬식: {int(round(get_d))}")
else:
    print(f" -> 행렬식: {round(get_d, 4)}")

if abs(get_d) < 1e-9:
    print("오류 : 역행렬이 존재하지 않는다 (행렬식은 0).")
    ans1 = None
else:
    ans1 = m_inv1(input_data)
    print_matrix(ans1)

t_end1 = time.time()
elapsed1 = (t_end1 - t_start1) * 1000


print("\n[방법2 : 가우스-조던]")
t_start2 = time.time()
ans2 = m_inv2(input_data)
t_end2 = time.time()
elapsed2 = (t_end2 - t_start2) * 1000

if ans2 is None:
    print("오류 : 역행렬이 존재하지 않는다.")
else:
    print_matrix(ans2)


print("\n[두 방법 결과 비교]")
if ans1 is None and ans2 is None:
    print("역행렬이 존재하지 않는다.")
else:
    if check_same(ans1, ans2):
        print("두 결과 동일")
    else:
        print("두 결과 다름")


if ans1 is not None and ans2 is not None:
    print(f"\n행렬식 방법 걸린 시간 : {round(elapsed1, 5)} ms")
    print(f"가우스-조던 방법 걸린 시간 : {round(elapsed2, 5)} ms")
    
    if elapsed1 > elapsed2:
        print(" -> 가우스-조던 방식이 더 빠르다.")
    elif elapsed2 > elapsed1:
        print(" -> 행렬식 방법이 더 빠르다.")
    else:
        print(" -> 두 방법 걸린 시간이 똑같다.")
else:
    print("역행렬이 존재하지 않는다.")
