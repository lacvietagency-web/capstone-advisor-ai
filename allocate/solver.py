"""Bộ giải bài toán phân công đề tài tốt nghiệp cho sinh viên.

Bao gồm:
    1. solve_ilp: Tối ưu hoá phân công bằng Quy hoạch nguyên tuyến tính (ILP / PuLP CBC).
    2. solve_greedy: Phân công tham lam dựa trên điểm cao nhất và GPA.
    3. metrics: Đánh giá chất lượng phân công (tỷ lệ xếp, đạt NV1, mean rank, quota violations...).
    4. suggest_remaining_topics: Gợi ý đề tài còn chỗ cho sinh viên chưa được xếp (pha 2).
"""

import pulp

BONUS_MAP = {1: 1.0, 2: 0.6, 3: 0.3}


def compute_utility(s, t, rank, scores, gpa, alpha=0.4, beta=0.6, eps=1e-3):
    """Tính điểm thoả dụng U(s, t) khi sinh viên s được gán vào đề tài t.

    Công thức:
        U(s, t) = alpha * (score(s, t) / 100) + beta * Bonus(rank) + eps * (gpa(s) / 4)
    với:
        - Bonus: NV1 = 1.0, NV2 = 0.6, NV3 = 0.3 (ngoài Top 3: 0.0)
        - score(s, t) trong khoảng [0, 100]
        - gpa(s) trong khoảng [0, 4]
    """
    score = scores.get((s, t), 0.0)
    bonus = BONUS_MAP.get(rank, 0.0)
    student_gpa = gpa.get(s, 0.0)
    return alpha * (score / 100.0) + beta * bonus + eps * (student_gpa / 4.0)


def _build_ilp_constraints(prob, prefs, x, u, cap, owner, quota):
    """Thêm các ràng buộc tuyến tính cho bài toán ILP.

    Ràng buộc:
        1. sum_{t in prefs[s]} x[s, t] + u[s] = 1 (mỗi SV nhận đúng 1 đề tài hoặc chưa xếp)
        2. sum_{s: t in prefs[s]} x[s, t] <= cap[t] (sức chứa từng đề tài)
        3. sum_{t: owner[t] = g} sum_s x[s, t] <= quota[g] (chỉ tiêu giảng viên)
    """
    for s, topic_list in prefs.items():
        prob += pulp.lpSum(x[s, t] for t in topic_list) + u[s] == 1

    topic_vars = {}
    lecturer_vars = {}
    for (_s, t), var in x.items():
        topic_vars.setdefault(t, []).append(var)
        g = owner.get(t)
        if g is not None:
            lecturer_vars.setdefault(g, []).append(var)

    for t, vars_list in topic_vars.items():
        if t in cap:
            prob += pulp.lpSum(vars_list) <= cap[t]

    for g, vars_list in lecturer_vars.items():
        if g in quota:
            prob += pulp.lpSum(vars_list) <= quota[g]


def solve_ilp(prefs, scores, cap, owner, quota, gpa, alpha=0.4, beta=0.6, lam=None, eps=1e-3, ranks=None):
    """Phân công đề tài bằng quy hoạch nguyên tuyến tính (PuLP + CBC).

    `ranks[(s, t)]` = thứ tự NV thật của SV (1–3). prefs đã bỏ NV bị GV từ chối / không đủ điều kiện, nên vị trí
    trong prefs có thể nhỏ hơn thứ tự thật (NV1 bị từ chối → NV2 đứng đầu); Bonus tính theo thứ tự thật như báo cáo.
    Không truyền ranks (dữ liệu thực nghiệm không có NV bị loại) thì dùng vị trí trong prefs.

    Mục tiêu:
        max sum_{s, t} x[s, t] * U(s, t) - lam * sum_s u[s]
    với U(s, t) = alpha * (score / 100) + beta * Bonus + eps * (gpa / 4) ≤ alpha + beta + eps.
    Ưu tiên tối đa số SV được xếp (rồi mới tới độ thoả dụng) cần lam > n·(alpha + beta + eps), n = số SV: xếp thêm 1 SV
    (+lam) khi đó luôn hơn mọi phần thoả dụng có thể mất khi dời các SV khác. lam cố định = 2 KHÔNG đủ: chuỗi 4 SV phải
    lùi NV1 → NV3 để nhường chỗ (mất 4 × 0,82 > 2 + 1) thì ILP bỏ 1 SV dù xếp được hết (test V39MaxCoverage).
    Mặc định lam = 1 + n·(alpha + beta + eps); truyền lam để tái lập thí nghiệm cũ.
    """
    if not prefs:
        return {}
    if lam is None:
        lam = 1.0 + len(prefs) * (alpha + beta + eps)

    prob = pulp.LpProblem("Topic_Allocation", pulp.LpMaximize)

    x = {}
    u = {}
    obj_terms = []

    for i, (s, topic_list) in enumerate(prefs.items()):
        u[s] = pulp.LpVariable(f"u_{i}", cat=pulp.LpBinary)
        obj_terms.append(-lam * u[s])
        for j, t in enumerate(topic_list):
            x[s, t] = pulp.LpVariable(f"x_{i}_{j}", cat=pulp.LpBinary)
            rank = ranks.get((s, t), j + 1) if ranks else j + 1
            utility = compute_utility(s, t, rank, scores, gpa, alpha, beta, eps)
            obj_terms.append(x[s, t] * utility)

    prob += pulp.lpSum(obj_terms)
    _build_ilp_constraints(prob, prefs, x, u, cap, owner, quota)

    solver = pulp.PULP_CBC_CMD(msg=False)
    prob.solve(solver)

    assigned = {}
    for s, topic_list in prefs.items():
        assigned_topic = None
        for t in topic_list:
            val = pulp.value(x[s, t])
            if val is not None and val > 0.5:
                assigned_topic = t
                break
        assigned[s] = assigned_topic

    return assigned


def solve_greedy(prefs, scores, cap, owner, quota, gpa):
    """Phân công đề tài theo thuật toán tham lam (Greedy).

    Sắp xếp SV theo điểm cao nhất của các NV giảm dần (hòa điểm thì xét GPA giảm dần).
    Gán lần lượt NV1 -> NV2 -> NV3 nếu đề tài còn chỗ và giảng viên còn chỉ tiêu.
    """
    if not prefs:
        return {}

    def student_sort_key(s):
        student_prefs = prefs.get(s, [])
        max_score = max((scores.get((s, t), 0.0) for t in student_prefs), default=0.0)
        student_gpa = gpa.get(s, 0.0)
        return (-max_score, -student_gpa, str(s))

    sorted_students = sorted(prefs.keys(), key=student_sort_key)
    rem_cap = dict(cap)
    rem_quota = dict(quota)
    assigned = {s: None for s in prefs}

    for s in sorted_students:
        for t in prefs.get(s, []):
            g = owner.get(t)
            topic_ok = rem_cap.get(t, 0) > 0
            lecturer_ok = (g is None) or (rem_quota.get(g, 0) > 0)
            if topic_ok and lecturer_ok:
                assigned[s] = t
                rem_cap[t] -= 1
                if g is not None and g in rem_quota:
                    rem_quota[g] -= 1
                break

    return assigned


def _percentile(values, q):
    """Phân vị q (0–100), nội suy tuyến tính như numpy.percentile — tránh phụ thuộc numpy."""
    v = sorted(values)
    k = (len(v) - 1) * q / 100
    f = int(k)
    c = min(f + 1, len(v) - 1)
    return float(v[f] + (v[c] - v[f]) * (k - f))


def _count_quota_violations(topic_counts, cap, owner, quota):
    """Đếm tổng số vi phạm: số đề tài vượt sức chứa + số GV vượt chỉ tiêu."""
    violations = 0
    for t, cnt in topic_counts.items():
        if cnt > cap.get(t, 0):
            violations += 1

    lecturer_counts = {}
    for t, cnt in topic_counts.items():
        g = owner.get(t)
        if g is not None:
            lecturer_counts[g] = lecturer_counts.get(g, 0) + cnt

    for g, cnt in lecturer_counts.items():
        if cnt > quota.get(g, 0):
            violations += 1

    return violations


def metrics(assign, prefs, scores, cap, owner, quota, ranks=None):
    """Tính toán các chỉ số đánh giá phân công đề tài. `ranks[(s, t)]` = thứ tự NV thật (xem solve_ilp).

    Trả về dictionary gồm:
        - assigned_rate: Số SV được xếp / Tổng số SV
        - nv1_rate: Số SV đạt NV1 / Tổng số SV
        - top3_rate: Số SV đạt Top 3 / Tổng số SV
        - mean_rank: Thứ hạng NV trung bình tính trên SV được xếp
        - avg_match: Điểm phù hợp trung bình các cặp được xếp
        - p10_match: Phân vị thứ 10 của điểm phù hợp các cặp được xếp
        - quota_violations: Số GV vượt chỉ tiêu + đề tài vượt sức chứa
    """
    total_students = len(assign) if assign else len(prefs)
    if total_students == 0:
        return {
            "assigned_rate": 0.0,
            "nv1_rate": 0.0,
            "top3_rate": 0.0,
            "mean_rank": 0.0,
            "avg_match": 0.0,
            "p10_match": 0.0,
            "quota_violations": 0,
        }

    assigned_pairs = [(s, t) for s, t in assign.items() if t is not None]
    num_assigned = len(assigned_pairs)

    num_nv1 = 0
    num_top3 = 0
    rank_list = []
    match_scores = []
    topic_counts = {}

    for s, t in assigned_pairs:
        st_prefs = prefs.get(s, [])
        if t in st_prefs:
            r = ranks.get((s, t), st_prefs.index(t) + 1) if ranks else st_prefs.index(t) + 1
            rank_list.append(r)
            if r == 1:
                num_nv1 += 1
            if r <= 3:
                num_top3 += 1
        match_scores.append(float(scores.get((s, t), 0.0)))
        topic_counts[t] = topic_counts.get(t, 0) + 1

    assigned_rate = num_assigned / total_students
    nv1_rate = num_nv1 / total_students
    top3_rate = num_top3 / total_students
    mean_rank = (sum(rank_list) / len(rank_list)) if rank_list else 0.0
    avg_match = (sum(match_scores) / len(match_scores)) if match_scores else 0.0
    p10_match = _percentile(match_scores, 10) if match_scores else 0.0
    quota_violations = _count_quota_violations(topic_counts, cap, owner, quota)

    return {
        "assigned_rate": assigned_rate,
        "nv1_rate": nv1_rate,
        "top3_rate": top3_rate,
        "mean_rank": mean_rank,
        "avg_match": avg_match,
        "p10_match": p10_match,
        "quota_violations": quota_violations,
    }


def suggest_remaining_topics(assigned, cap, owner, quota, scores=None):
    """Gợi ý danh sách đề tài còn chỗ cho các sinh viên chưa được xếp (pha 2).

    Đề tài còn chỗ khi số SV đã gán < cap[t] và giảng viên owner[t] chưa hết chỉ tiêu.
    """
    topic_counts = {}
    for t in assigned.values():
        if t is not None:
            topic_counts[t] = topic_counts.get(t, 0) + 1

    lecturer_counts = {}
    for t, cnt in topic_counts.items():
        g = owner.get(t)
        if g is not None:
            lecturer_counts[g] = lecturer_counts.get(g, 0) + cnt

    available_topics = []
    for t, capacity in cap.items():
        used_cap = topic_counts.get(t, 0)
        g = owner.get(t)
        used_quota = lecturer_counts.get(g, 0) if g is not None else 0
        quota_max = quota.get(g, 0) if g is not None else 999
        if used_cap < capacity and used_quota < quota_max:
            available_topics.append(t)

    unassigned_students = [s for s, t in assigned.items() if t is None]
    suggestions = {}
    for s in unassigned_students:
        if scores is not None:
            sorted_topics = sorted(
                available_topics, key=lambda t, current_s=s: scores.get((current_s, t), 0.0), reverse=True
            )
        else:
            sorted_topics = list(available_topics)
        suggestions[s] = sorted_topics

    return suggestions
