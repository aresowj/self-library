using System;

namespace Utility
{
    public class DateTimeUtility
    {
        private static readonly DateTime _Epoch = new DateTime(1970, 1, 1, 0, 0, 0, DateTimeKind.Utc);
        public static DateTime Epoch { get { return _Epoch;  } }
        
        public static DateTime GetDateTimeFromTimestamp(string timestamp)
        {
            return GetDateTimeFromTimestamp(double.Parse(timestamp));
        }

        public static DateTime GetDateTimeFromTimestamp(double seconds)
        {
            return Epoch.AddSeconds(seconds);
        }
    }
}
