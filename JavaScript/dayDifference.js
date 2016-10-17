function dayDifference(start, end) {
    // Input date must be Date instance. Set time to 00:00:00
    // to consider only the date difference.
    start.setHours(0);
    start.setMinutes(0);
    start.setSeconds(0);

    return Math.round((end - start) / DAY_TO_MILLISECONDS);
}
