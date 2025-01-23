import React, { useMemo } from "react";
import { View, Text, StyleSheet, ScrollView } from "react-native";

// Example: We'll assume times from 7:00 PM (19 in 24-hour) on one day
// to 6:00 AM (6 in 24-hour) next day, but do it in 30-min increments.
const START_HOUR_24 = 8; // 8 AM
const END_HOUR_24 = 23; // 11 PM

/**
 * A single row of horizontally scrollable half-hour slots, each colored
 * green if free, red if a meeting starts at that half-hour.
 */
export default function AvailabilityGrid({ room }) {
  // We have a small explanation at the top
  // "A time is red if a meeting starts at that time"

  // Convert each meeting start time into a minute-of-day for quick comparison
  const meetingStartOffsets = useMemo(() => {
    return room.meetings.map((m) => parseTimeToMinutes(m.MtgStartTime));
  }, [room.meetings]);

  // Build a list of half-hour increments
  // e.g. 7:00 PM -> 19:00, 7:30 -> 19:30, 8:00 -> 20:00, … up to 6:00 next day
  const slots = useMemo(() => {
    const result = [];
    let currentHour = START_HOUR_24;
    let currentMinute = 0; // 0 or 30
    // We'll loop until we wrap around to END_HOUR_24 in hours
    while (true) {
      result.push({ hour24: currentHour, minute: currentMinute });
      // Move forward 30 min
      currentMinute += 30;
      if (currentMinute >= 60) {
        currentMinute = 0;
        currentHour = (currentHour + 1) % 24;
      }
      // Check if we reached or passed END_HOUR_24 with hour+minute=0
      if (currentHour === END_HOUR_24 && currentMinute === 0) {
        break;
      }
    }
    return result;
  }, []);

  /**
   * Tells us if a meeting starts exactly at this half-hour slot.
   * We compare to the meetingStartOffsets array.
   */
  function isMeetingStart(hour24, min) {
    const offset = hour24ToAbsoluteMin(hour24) + min;
    return meetingStartOffsets.includes(offset);
  }

  return (
    <View style={styles.container}>


      <Text style={styles.roomTitle}>Availibility:</Text>

      <ScrollView horizontal showsHorizontalScrollIndicator={true}>
        <View style={styles.rowContainer}>
          {slots.map((slot, index) => {
            const { hour24, minute } = slot;
            const busy = isMeetingStart(hour24, minute);
            const label = formatHalfHour(hour24, minute);
            return (
              <View
                key={index}
                style={[
                  styles.slotCell,
                  { backgroundColor: busy ? "red" : "green" },
                ]}
              >
                <Text style={styles.slotLabel}>{label}</Text>
              </View>
            );
          })}
        </View>
      </ScrollView>
    </View>
  );
}

/** Convert "9:00 PM" -> an absolute minute of the day (0..1439). */
function parseTimeToMinutes(timeStr) {
  // Basic parse: "HH:MM AM/PM"
  const [timePart, ampmPart] = timeStr.split(" ");
  const [hourStr, minStr] = timePart.split(":");
  let hour = parseInt(hourStr, 10) % 12; // 12 -> 0
  const minute = parseInt(minStr, 10) || 0;
  if ((ampmPart || "").toUpperCase() === "PM") hour += 12;
  return hour * 60 + minute;
}

/** Convert an hour24 (0..23) into absolute minutes for that day. */
function hour24ToAbsoluteMin(hour24) {
  return hour24 * 60;
}

/** Format "19,30" => "7:30 PM", "0,0" => "12 AM" */
function formatHalfHour(hour24, minute) {
  // Convert 24-hr to 12-hr
  let h12 = hour24 % 12;
  if (h12 === 0) h12 = 12;
  const ampm = hour24 < 12 ? "AM" : "PM";
  if (minute === 0) {
    return `${h12} ${ampm}`;
  }
  // e.g. "7:30 PM"
  return `${h12}:${minute < 10 ? "0" : ""}${minute} ${ampm}`;
}

const styles = StyleSheet.create({
  container: {
    marginVertical: 12,
    marginHorizontal: 0,
  },
  infoText: {
    marginBottom: 6,
    fontSize: 14,
  },
  roomTitle: {
    fontSize: 16,
    fontWeight: "bold",
    marginBottom: 6,
  },
  rowContainer: {
    flexDirection: "row",
  },
  slotCell: {
    width: 65,
    height: 40,
    justifyContent: "center",
    alignItems: "center",
    marginRight: 2,
  },
  slotLabel: {
    color: "#fff",
    fontWeight: "600",
  },
});
