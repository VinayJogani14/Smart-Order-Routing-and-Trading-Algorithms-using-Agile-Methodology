def plan_pov(total_qty, rate, volumes):
    filled = 0
    schedule = []
    for v in volumes:
        q = min(total_qty - filled, rate * v)
        schedule.append(q)
        filled += q
        if filled >= total_qty:
            break
    return schedule + [0]*(len(volumes) - len(schedule))