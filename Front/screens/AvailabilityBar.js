// File: AvailabilityBar.js
import React from "react";
import { StyleSheet, View } from "react-native";
import { Text } from "react-native-paper";
import dayjs from "dayjs";
import customParseFormat from "dayjs/plugin/customParseFormat";
dayjs.extend(customParseFormat);

// 1) We define our day range: 8 AM to 11 PM (same day)
const START_TIME = dayjs().hour(8).minute(0).second(0).millisecond(0);
const END_TIME = dayjs().hour(23).minute(0).second(0).millisecond(0);

// 2) Calculate total minutes in the window
const TOTAL_MINUTES = END_TIME.diff(START_TIME, "minute"); // 8 AM–11 PM = 900 min

// 3) We'll define a bar width
const BAR_WIDTH = 300;
const MINUTE_WIDTH = BAR_WIDTH / TOTAL_MINUTES;

// Parse time strings like "10:00 AM" or "9:30 AM"
function parseTime(timeStr) {
  // Try both one-digit and two-digit hour
  const parsed = dayjs(timeStr, ["h:mm A", "hh:mm A"], true);
  if (!parsed.isValid()) {
    console.warn("Invalid time:", timeStr);
  }
  return parsed;
}

export default function AvailabilityBar({ room }) {
  // 'room' might be:
  // {
  //   roomNum: 'BLAU0560',
  //   meetings: [
  //     { MtgStartTime: '10:00 AM', MtgEndTime: '12:00 PM' },
  //     { MtgStartTime: '2:30 PM', MtgEndTime: '4:00 PM' },
  //   ]
  // }

  return (
    <View style={styles.container}>
      {/* Paper’s Text with a slightly bigger style variant */}
      <Text variant="titleMedium" style={styles.title}>
        Room: {room.roomNum}
      </Text>

      <View style={styles.outerBar}>
        {/* Entire bar green by default */}
        <View style={[styles.bar, { backgroundColor: "green" }]} />

        {/* Render a red overlay for each busy segment */}
        {room.meetings.map((mtg, idx) => {
          console.log("Start:", mtg.MtgStartTime, "End:", mtg.MtgEndTime);
          const left = timeToXPos(mtg.MtgStartTime);
          const width = calculateWidth(mtg.MtgStartTime, mtg.MtgEndTime);

          console.log("left:", left, "width:", width);

          return (
            <View
              key={idx}
              style={[
                styles.busySegment,
                {
                  left: left,
                  width: width,
                },
              ]}
            />
          );
        })}
      </View>
    </View>
  );
}

// Helper: Convert "10:00 AM" to dayjs, then compute X offset in px
function timeToXPos(timeStr) {
  const timeObj = parseTime(timeStr);
  if (!timeObj.isValid()) return 0; // fallback
  let offsetMin = timeObj.diff(START_TIME, "minute");
  offsetMin = clamp(offsetMin, 0, TOTAL_MINUTES);
  return offsetMin * MINUTE_WIDTH;
}

// Helper: Calculate overlay width from startTime to endTime
function calculateWidth(startStr, endStr) {
  const startObj = parseTime(startStr);
  const endObj = parseTime(endStr);

  let startMin = startObj.diff(START_TIME, "minute");
  let endMin = endObj.diff(START_TIME, "minute");

  startMin = clamp(startMin, 0, TOTAL_MINUTES);
  endMin = clamp(endMin, 0, TOTAL_MINUTES);

  return Math.max(0, endMin - startMin) * MINUTE_WIDTH;
}

// Simple clamp function
function clamp(value, min, max) {
  return Math.max(min, Math.min(value, max));
}

// Styles
const styles = StyleSheet.create({
  container: {
    marginVertical: 12,
  },
  title: {
    marginBottom: 4,
  },
  outerBar: {
    width: BAR_WIDTH,
    height: 20,
    position: "relative",
    borderWidth: 1,
    borderColor: "#ccc",
  },
  bar: {
    ...StyleSheet.absoluteFillObject,
  },
  busySegment: {
    position: "absolute",
    top: 0,
    bottom: 0,
    backgroundColor: "red",
  },
});
