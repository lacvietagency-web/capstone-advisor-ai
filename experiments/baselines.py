"""Hai thuật toán đối chứng cho RQ3b (theo thuyết minh đề tài): Gale-Shapley (SPA-student) và Giải thuật di truyền (GA).

Dùng cùng dữ liệu với allocate.solver: prefs[s] = [t1, t2, t3], scores[(s, t)], cap[t], owner[t] = g, quota[g], gpa[s].

Thứ tự ưu tiên của giảng viên (bắt buộc với Gale-Shapley, dùng để đếm cặp chặn cho mọi thuật toán):
GV g xếp SV theo điểm phù hợp cao nhất của SV với các đề tài của g mà SV đã chọn, hoà thì GPA cao hơn, rồi mã SV.
"""

import random

from allocate.solver import compute_utility


def lecturer_rankings(prefs, scores, owner, gpa):
    """rank[g][s] = vị trí của SV s trong danh sách ưu tiên của GV g (0 = được ưu tiên nhất)."""
    best = {}
    for s, ts in prefs.items():
        for t in ts:
            g = owner.get(t)
            best[g, s] = max(best.get((g, s), -1.0), scores.get((s, t), 0.0))
    by_g = {}
    for (g, s), sc in best.items():
        by_g.setdefault(g, []).append((-sc, -gpa.get(s, 0.0), str(s), s))
    return {g: {item[3]: i for i, item in enumerate(sorted(lst))} for g, lst in by_g.items()}


def solve_gale_shapley(prefs, scores, cap, owner, quota, gpa):  # noqa: C901 — đúng từng bước thuật toán gốc
    """Thuật toán SPA-student (Abraham, Irving & Manlove, 2007): ghép cặp ỔN ĐỊNH, tối ưu phía sinh viên,
    tôn trọng sức chứa đề tài và chỉ tiêu giảng viên."""
    from collections import deque

    rank = lecturer_rankings(prefs, scores, owner, gpa)
    lists = {s: list(ts) for s, ts in prefs.items()}
    on_p, on_l, assigned = {}, {}, {s: None for s in prefs}

    def worst(g, group):
        return max(group, key=lambda x: rank[g][x])

    def drop(r):
        t = assigned[r]
        on_p[t].discard(r)
        on_l[owner.get(t)].discard(r)
        assigned[r] = None
        free.append(r)

    free = deque(prefs)
    while free:
        s = free.popleft()
        if assigned[s] is not None or not lists[s]:
            continue
        t = lists[s][0]
        g = owner.get(t)
        assigned[s] = t
        on_p.setdefault(t, set()).add(s)
        on_l.setdefault(g, set()).add(s)
        if len(on_p[t]) > cap.get(t, 0):  # đề tài quá tải → GV bỏ SV kém nhất của đề tài
            drop(worst(g, on_p[t]))
        elif len(on_l[g]) > quota.get(g, 0):  # GV quá chỉ tiêu → bỏ SV kém nhất của GV
            drop(worst(g, on_l[g]))
        if on_p[t] and len(on_p[t]) == cap.get(t, 0):  # đề tài đầy: SV kém hơn SV kém nhất không còn cơ hội với t
            w = rank[g][worst(g, on_p[t])]
            for st, lst in lists.items():
                if t in lst and rank[g].get(st, 10**9) > w:
                    lst.remove(t)
        if on_l[g] and len(on_l[g]) == quota.get(g, 0):  # GV đủ chỉ tiêu: SV kém hơn mất mọi đề tài của GV
            w = rank[g][worst(g, on_l[g])]
            for st in lists:
                if rank[g].get(st, 10**9) > w:
                    lists[st] = [x for x in lists[st] if owner.get(x) != g]
    return assigned


def solve_genetic(  # noqa: C901 — giải mã + sửa nghiệm + vòng tiến hoá, giữ liền cho dễ đối chiếu
    prefs,
    scores,
    cap,
    owner,
    quota,
    gpa,
    alpha=0.4,
    beta=0.6,
    eps=1e-3,
    pop_size=60,
    generations=150,
    mutation=None,
    seed=0,
):
    """Giải thuật di truyền: gen = chỉ số NV (0..2) hoặc 3 = chưa xếp. Giải mã có bước SỬA để luôn hợp lệ
    (đề tài/GV quá tải thì bỏ SV có thoả dụng thấp nhất). Thích nghi = cùng hàm mục tiêu với ILP:
    Σ U(s, t) − λ·(số SV chưa xếp), λ = 1 + n(α + β + ε).
    Chọn lọc giải đấu, lai đều, đột biến 1/n, giữ 2 cá thể tốt nhất.
    ponytail: Python thuần, quy mô 1.000 SV mất vài chục giây — đủ cho thực nghiệm, không dùng trong ứng dụng."""
    rnd = random.Random(seed)
    students = list(prefs)
    n = len(students)
    if n == 0:
        return {}
    lam = 1.0 + n * (alpha + beta + eps)
    util = {
        (s, t): compute_utility(s, t, j + 1, scores, gpa, alpha, beta, eps)
        for s in students
        for j, t in enumerate(prefs[s])
    }
    mutation = mutation if mutation is not None else 1.0 / n

    def decode(genes):  # noqa: C901
        a = {}
        for s, gidx in zip(students, genes, strict=True):
            a[s] = prefs[s][gidx] if gidx < len(prefs[s]) else None
        by_t, by_g = {}, {}
        for s, t in a.items():
            if t is not None:
                by_t.setdefault(t, []).append(s)
        for t, ss in by_t.items():  # sửa: đề tài quá sức chứa
            if len(ss) > cap.get(t, 0):
                ss.sort(key=lambda x, t=t: util[x, t], reverse=True)
                for x in ss[cap.get(t, 0) :]:
                    a[x] = None
        for s, t in a.items():
            if t is not None:
                by_g.setdefault(owner.get(t), []).append(s)
        for g, ss in by_g.items():  # sửa: GV quá chỉ tiêu
            if len(ss) > quota.get(g, 0):
                ss.sort(key=lambda x: util[x, a[x]], reverse=True)
                for x in ss[quota.get(g, 0) :]:
                    a[x] = None
        fit = sum(util[s, t] for s, t in a.items() if t is not None) - lam * sum(1 for t in a.values() if t is None)
        return fit, a

    pop = [[rnd.randrange(len(prefs[s])) if rnd.random() < 0.9 else 3 for s in students] for _ in range(pop_size)]
    scored = sorted(((decode(g)[0], g) for g in pop), key=lambda x: -x[0])
    for _ in range(generations):
        nxt = [scored[0][1], scored[1][1]]
        while len(nxt) < pop_size:
            p1 = max(rnd.sample(scored, 3), key=lambda x: x[0])[1]
            p2 = max(rnd.sample(scored, 3), key=lambda x: x[0])[1]
            child = [a if rnd.random() < 0.5 else b for a, b in zip(p1, p2, strict=True)]
            for i in range(n):
                if rnd.random() < mutation:
                    child[i] = rnd.randrange(4)
            nxt.append(child)
        scored = sorted(((decode(g)[0], g) for g in nxt), key=lambda x: -x[0])
    return decode(scored[0][1])[1]


def blocking_pairs(assign, prefs, scores, cap, owner, quota, gpa):
    """Số cặp chặn (s, t) theo định nghĩa ổn định của SPA (Abraham và cộng sự, 2007): s muốn t hơn đề tài hiện tại
    (hoặc đang chưa có), và t còn chỗ + GV còn chỉ tiêu, hoặc GV sẵn lòng đổi một SV kém hơn lấy s."""
    rank = lecturer_rankings(prefs, scores, owner, gpa)
    on_p, on_l = {}, {}
    for s, t in assign.items():
        if t is not None:
            on_p.setdefault(t, []).append(s)
            on_l.setdefault(owner.get(t), []).append(s)
    count = 0
    for s, ts in prefs.items():
        cur = assign.get(s)
        better = ts if cur is None else ts[: ts.index(cur)] if cur in ts else ts
        for t in better:
            g = owner.get(t)
            p_full = len(on_p.get(t, [])) >= cap.get(t, 0)
            l_full = len(on_l.get(g, [])) >= quota.get(g, 0)
            worse_than = lambda grp, g=g, s=s: any(rank[g][x] > rank[g][s] for x in grp)  # noqa: E731
            free_slot = not p_full and not l_full
            swap_in_lecturer = not p_full and l_full and (owner.get(cur) == g or worse_than(on_l.get(g, [])))
            swap_in_topic = p_full and worse_than(on_p.get(t, []))
            if free_slot or swap_in_lecturer or swap_in_topic:
                count += 1
    return count


def load_spread(assign, owner, quota):
    """Độ lệch tải GV: độ lệch chuẩn của (số SV được xếp / chỉ tiêu) trên các GV có chỉ tiêu."""
    load = {g: 0 for g in quota}
    for t in assign.values():
        if t is not None and owner.get(t) in load:
            load[owner[t]] += 1
    r = [load[g] / quota[g] for g in quota if quota[g]]
    m = sum(r) / len(r)
    return (sum((x - m) ** 2 for x in r) / len(r)) ** 0.5
