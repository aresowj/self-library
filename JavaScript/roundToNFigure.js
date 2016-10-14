function roundToNFigure(num) {
    / * Convert a number to its nearest N figure .
      * For example, 4 => 10, 45 => 50, 1922 => 2000 ...
      * /
    var max_len = num.toString().split(".")[0].length - 1;
    if (max_len <= 0) max_len = 1;
    var factor = Math.pow(10, max_len);
    num = Math.ceil(num / factor) * factor;

    return num;
}
