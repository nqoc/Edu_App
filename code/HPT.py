import streamlit as st
import pandas as pd
import numpy as np

def solve(coefficients, constants):
    try:
        n = len(coefficients)
        A = [[coefficients[i][j] for j in range(n)] for i in range(n)]
        B = constants.copy()

        for i in range(n):
            max_element = abs(A[i][i])
            max_row = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > max_element:
                    max_element = abs(A[j][i])
                    max_row = j

            for j in range(i, n):
                A[max_row][j], A[i][j] = A[i][j], A[max_row][j]
            B[max_row], B[i] = B[i], B[max_row]

            for j in range(i + 1, n):
                factor = A[j][i] / A[i][i]
                B[j] -= factor * B[i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]

        x = [0] * n
        for i in range(n - 1, -1, -1):
            s = sum(A[i][j] * x[j] for j in range(i, n))
            x[i] = (B[i] - s) / A[i][i]
        return tuple(x)
    except ZeroDivisionError:
        if all([bool(x==0) for x in B]):
            return "Hệ phương trình đã cho vô số nghiệm"
        else:
            return "Hệ phương trình đã cho vô nghiệm"


abc="abcdefghijkllmnopqrstuvwxyz"
st.title("Giải hệ phương trình bậc nhất n ẩn")
st.divider()
st.caption("Designed By H-DesignerIT")

n = int(st.number_input("Nhập số lượng ẩn trong hệ phương trình: ",min_value=1,max_value=20,step=1))
A = []
B = []

for i in range(n):
    row = []
    for j in range(n):
        val = float(st.number_input("Nhập giá trị A[{}][{}]: ".format(i+1, j+1),format="%.5f"))
        row.append(val)
    A.append(row)
    val = float(st.number_input("Nhập giá trị B[{}]: ".format(i+1),format="%.5f"))
    B.append(val)

if st.button("Giải"):
    X = solve(A, B)
    if type(X)!=type(""):
        for i in range(n):
            A[i].append(B[i])

        df = pd.DataFrame(np.array(A),columns=(i for i in abc[:n+1]))
        st.table(df)
        st.write("Nghiệm của hệ phương trình là: ")
        for i in range(n):
            st.metric(label="x[{}]".format(i+1), value="{}".format(X[i]))
    else:
        st.write(X)