"""Mô-đun tính toán trọng số theo phương pháp Phân tích Thứ bậc (AHP - Analytic Hierarchy Process).

Phương pháp AHP của Thomas L. Saaty (1980):
1. Nhận ma trận so sánh cặp A kích thước n×n (n=5 tương ứng với 5 tiêu chí: skill, academic, field, semantic, llm)
   trên thang điểm Saaty 1–9, thoả mãn tính nghịch đảo a_ij = 1 / a_ji và a_ii = 1.
2. Xác định vector trọng số w:
   - Phương pháp trị riêng chính (Principal Eigenvector):
     A * w = λ_max * w
     Chuẩn hoá vector riêng w sao cho tổng các phần tử bằng 1.
   - Phương pháp trung bình hình học (Geometric Mean):
     r_i = (∏_{j=1}^n a_ij)^(1/n)
     w_i = r_i / ∑_{k=1}^n r_k
     λ_max = (1/n) * ∑_{i=1}^n ((A * w)_i / w_i)
3. Tính chỉ số nhất quán (Consistency Index - CI):
   CI = (λ_max - n) / (n - 1)
4. Tính tỷ số nhất quán (Consistency Ratio - CR):
   CR = CI / RI
   Với n = 5, chỉ số ngẫu nhiên chuẩn RI = 1.12.
5. Kiểm tra tính nhất quán:
   Nếu CR < 0.1: ma trận đạt độ nhất quán tin cậy.
   Nếu CR >= 0.1: ma trận thiếu nhất quán, bị từ chối.
"""

from fractions import Fraction
from typing import NamedTuple

import numpy as np

# 5 tiêu chí đánh giá đề tài tốt nghiệp
CRITERIA = ("skill", "academic", "field", "semantic", "llm")

# Chỉ số ngẫu nhiên RI (Random Index) theo Saaty cho kích thước ma trận n = 1..10
RI_TABLE = {
    1: 0.0,
    2: 0.0,
    3: 0.58,
    4: 0.90,
    5: 1.12,
    6: 1.24,
    7: 1.32,
    8: 1.41,
    9: 1.45,
    10: 1.49,
}
RI_5 = 1.12
CR_THRESHOLD = 0.1


class AHPResult(NamedTuple):
    """Kết quả tính toán AHP gồm vector trọng số, λ_max, CI và CR."""

    weights: dict[str, float]
    lambda_max: float
    ci: float
    cr: float

    @property
    def is_consistent(self) -> bool:
        """Kiểm tra ma trận có đạt độ nhất quán (CR < 0.1) hay không."""
        return self.cr < CR_THRESHOLD


def _parse_cell(val) -> float:
    """Chuyển đổi một phần tử trong ma trận về số thực (hỗ trợ phân số dạng chuỗi như '1/3')."""
    if isinstance(val, (int, float)):
        return float(val)
    if isinstance(val, str):
        val_str = val.strip()
        if "/" in val_str:
            return float(Fraction(val_str))
        return float(val_str)
    raise TypeError(f"Không thể chuyển đổi giá trị '{val}' về float.")


def parse_matrix(data) -> np.ndarray:
    """Chuyển đổi dữ liệu ma trận đầu vào (danh sách hoặc từ điển) thành mảng numpy 2 chiều."""
    if isinstance(data, dict) and "matrix" in data:
        data = data["matrix"]
    if not isinstance(data, (list, tuple, np.ndarray)):
        raise TypeError("Dữ liệu ma trận phải là list, tuple hoặc np.ndarray.")
    raw_list = [[_parse_cell(item) for item in row] for row in data]
    return np.array(raw_list, dtype=float)


def validate_matrix(matrix: np.ndarray, expected_n: int = 5) -> None:
    """Kiểm tra tính hợp lệ của ma trận so sánh cặp n×n:

    - Đúng kích thước expected_n × expected_n (mặc định 5x5).
    - Mọi phần tử đều mang giá trị dương (> 0).
    - Đường chéo chính đều bằng 1.0 (a_ii = 1).
    - Tính nghịch đảo a_ij · a_ji = 1.
    """
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError(f"Ma trận phải là ma trận vuông {expected_n}x{expected_n}, nhận được dạng {matrix.shape}.")
    n = matrix.shape[0]
    if n != expected_n:
        raise ValueError(f"Kích thước ma trận là {n}x{n}, kỳ vọng {expected_n}x{expected_n}.")
    if np.any(matrix <= 0):
        raise ValueError("Tất cả các phần tử trong ma trận so sánh cặp phải lớn hơn 0.")
    if not np.allclose(np.diag(matrix), 1.0, atol=1e-3):
        raise ValueError("Các phần tử trên đường chéo chính của ma trận so sánh cặp phải bằng 1.")
    if not np.allclose(matrix * matrix.T, 1.0, atol=1e-2):  # a_ij · a_ji = 1 (cho phép làm tròn 1/3 ≈ 0.33)
        raise ValueError("Ma trận phải nghịch đảo: a_ij = 1 / a_ji.")


def calculate_ahp(matrix, criteria: tuple[str, ...] = CRITERIA, raise_on_inconsistent: bool = False) -> AHPResult:
    """Tính vector trọng số và kiểm định tỷ số nhất quán CR bằng phương pháp trị riêng (Eigenvector).

    Công thức:
        A * w = λ_max * w  (w > 0, ∑ w_i = 1)
        CI = (λ_max - n) / (n - 1)
        CR = CI / RI  (với n=5 thì RI=1.12)

    Nếu raise_on_inconsistent=True và CR >= 0.1, hàm sẽ ném ngoại lệ ValueError.
    """
    mat = parse_matrix(matrix)
    n = len(criteria)
    validate_matrix(mat, expected_n=n)

    eigvals, eigvecs = np.linalg.eig(mat)
    max_idx = int(np.argmax(eigvals.real))
    lambda_max = float(eigvals[max_idx].real)

    vec = eigvecs[:, max_idx].real
    if np.sum(vec) < 0:
        vec = -vec
    vec = np.maximum(vec, 0.0)
    w_arr = vec / np.sum(vec)

    ci = max(0.0, (lambda_max - n) / (n - 1)) if n > 1 else 0.0
    ri = RI_TABLE.get(n, RI_5)
    cr = (ci / ri) if ri > 0 else 0.0

    weights = {criteria[i]: float(w_arr[i]) for i in range(n)}
    result = AHPResult(weights=weights, lambda_max=lambda_max, ci=ci, cr=cr)

    if raise_on_inconsistent and not result.is_consistent:
        raise ValueError(f"Ma trận thiếu nhất quán (CR = {cr:.4f} >= 0.1), bị từ chối.")
    return result


def calculate_ahp_geometric(
    matrix, criteria: tuple[str, ...] = CRITERIA, raise_on_inconsistent: bool = False
) -> AHPResult:
    """Tính vector trọng số và kiểm định tỷ số nhất quán CR bằng phương pháp trung bình hình học (Geometric Mean).

    Công thức:
        r_i = (∏_{j=1}^n a_ij)^(1/n)
        w_i = r_i / ∑_{k=1}^n r_k
        λ_max = (1/n) * ∑_{i=1}^n ((A * w)_i / w_i)
        CI = (λ_max - n) / (n - 1)
        CR = CI / RI  (RI=1.12 cho n=5)
    """
    mat = parse_matrix(matrix)
    n = len(criteria)
    validate_matrix(mat, expected_n=n)

    geom = np.prod(mat, axis=1) ** (1.0 / n)
    w_arr = geom / np.sum(geom)

    mat_w = mat @ w_arr
    lambda_max = float(np.mean(mat_w / w_arr))

    ci = max(0.0, (lambda_max - n) / (n - 1)) if n > 1 else 0.0
    ri = RI_TABLE.get(n, RI_5)
    cr = (ci / ri) if ri > 0 else 0.0

    weights = {criteria[i]: float(w_arr[i]) for i in range(n)}
    result = AHPResult(weights=weights, lambda_max=lambda_max, ci=ci, cr=cr)

    if raise_on_inconsistent and not result.is_consistent:
        raise ValueError(f"Ma trận thiếu nhất quán (CR = {cr:.4f} >= 0.1), bị từ chối.")
    return result


# Định danh tương đương cho hàm tính AHP
compute_ahp = calculate_ahp
