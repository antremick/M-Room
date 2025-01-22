// File: AvailabilityBar.js
import React from "react";
import { StyleSheet, View } from "react-native";
import { Text } from "react-native-paper";
import dayjs from "dayjs";
import customParseFormat from "dayjs/plugin/customParseFormat";
dayjs.extend(customParseFormat);

// 1) Day range: 8 AM to 11 PM
const START_TIME = dayjs().hour(8).minute(0).second(0).millisecond(0);
const END_TIME = dayjs().hour(23).minute(0).second(0).millisecond(0);

// 2) Total minutes in [8 AM, 11 PM]
const TOTAL_MINUTES = END_TIME.diff(START_TIME, "minute"); // 8–23 = 900 min

// 3) Bar width
const BAR_WIDTH = 300;
const MINUTE_WIDTH = BAR_WIDTH / TOTAL_MINUTES;

// The break between 8 AM and 12 PM is 4 hours = 240 min => offset in px
const NOON_OFFSET = 240 * MINUTE_WIDTH;

export default function AvailabilityBar({ room }) {
  // We gather tick labels for bar edges and meeting edges
  let ticks = [
    { timeStr: "8:00 AM", left: 0, anchorEnd: false, isBarEdge: true },
    { timeStr: "11:00 PM", left: BAR_WIDTH, anchorEnd: true, isBarEdge: true },
  ];

  // Collect offsets to skip end=nextStart
  const startOffsets = [];
  const endOffsets = [];

  room.meetings.forEach((mtg) => {
    startOffsets.push(timeToXPos(mtg.MtgStartTime));
    endOffsets.push(timeToXPos(mtg.MtgEndTime));
  });

  // Add meeting times, skipping identical end = next start
  room.meetings.forEach((mtg) => {
    const startLeft = timeToXPos(mtg.MtgStartTime);
    const endLeft = timeToXPos(mtg.MtgEndTime);

    // Always add start
    ticks.push({
      timeStr: mtg.MtgStartTime,
      left: startLeft,
      isBarEdge: false,
    });

    // Add end only if no meeting starts at exactly the same offset
    if (!startOffsets.includes(endLeft)) {
      ticks.push({ timeStr: mtg.MtgEndTime, left: endLeft, isBarEdge: false });
    }
  });

  // Sort them by left offset
  ticks.sort((a, b) => a.left - b.left);

  return (
    <View style={styles.container}>
      <Text variant="titleMedium" style={styles.title}>
        Availability:
      </Text>

      <View style={styles.barContainer}>
        {/* AM/PM labels at start of each section */}
        <Text style={[styles.amPmLabel, { left: 5 }]}>AM</Text>
        <Text style={[styles.amPmLabel, { left: NOON_OFFSET + 5 }]}>PM</Text>

        {/* Outer bar has two sections: 8–12, 12–11 */}
        <View style={styles.outerBar}>
          {/* 8–12 portion: light blue */}
          <View
            style={[
              styles.timeBlock,
              {
                left: 0,
                width: NOON_OFFSET,
                backgroundColor: "#90EE90", // light sky blue
              },
            ]}
          />
          {/* 12–11 portion: darker blue */}
          <View
            style={[
              styles.timeBlock,
              {
                left: NOON_OFFSET,
                width: BAR_WIDTH - NOON_OFFSET,
                backgroundColor: "green", // steel blue
              },
            ]}
          />

          {/* Red busy segments */}
          {room.meetings.map((mtg, idx) => {
            const left = timeToXPos(mtg.MtgStartTime);
            const width = calculateWidth(mtg.MtgStartTime, mtg.MtgEndTime);
            return (
              <View
                key={idx}
                style={[
                  styles.busySegment,
                  {
                    left,
                    width,
                  },
                ]}
              />
            );
          })}
        </View>

        {/* Tick labels */}
        {ticks.map((tick, index) => {
          const shiftLeft = tick.anchorEnd ? -40 : 0;
          return (
            <Text
              key={index}
              style={[
                styles.tickLabel,
                { left: tick.left, transform: [{ translateX: shiftLeft }] },
              ]}
            >
              {formatTime(tick.timeStr)}
            </Text>
          );
        })}
      </View>
    </View>
  );
}

/** Convert "10:00 AM" => offset in px */
function timeToXPos(timeStr) {
  const t = parseTime(timeStr);
  if (!t.isValid()) return 0;
  let offsetMin = t.diff(START_TIME, "minute");
  offsetMin = clamp(offsetMin, 0, TOTAL_MINUTES);
  return offsetMin * MINUTE_WIDTH;
}

/** Calculate the busy (red) segment width */
function calculateWidth(startStr, endStr) {
  const s = parseTime(startStr);
  const e = parseTime(endStr);
  let startMin = s.diff(START_TIME, "minute");
  let endMin = e.diff(START_TIME, "minute");

  startMin = clamp(startMin, 0, TOTAL_MINUTES);
  endMin = clamp(endMin, 0, TOTAL_MINUTES);

  return Math.max(0, endMin - startMin) * MINUTE_WIDTH;
}

/** If it's "10:00 AM" or "9:30 AM", parse with dayjs. */
function parseTime(timeStr) {
  const parsed = dayjs(timeStr, ["h:mm A", "hh:mm A"], true);
  if (!parsed.isValid()) console.warn("Invalid time:", timeStr);
  return parsed;
}

/**
 * Formats the time with no "AM"/"PM" and skipping ":00" if on the hour
 * e.g. "8:00 AM" => "8", "9:30 AM" => "9:30", "11:15 PM" => "11:15"
 */
function formatTime(timeStr) {
  const t = parseTime(timeStr);
  if (!t.isValid()) return timeStr;
  const hour24 = t.hour(); // 0..23
  const minute = t.minute();

  // Convert 24-hr to 12-hr for display (without AM/PM text)
  let displayHour = hour24;
  if (displayHour === 0) displayHour = 12; // midnight
  if (displayHour > 12) displayHour -= 12;

  if (minute === 0) {
    return `${displayHour}`;
  } else {
    return `${displayHour}:${minute < 10 ? "0" : ""}${minute}`;
  }
}

/** Clamps to [min..max] */
function clamp(v, min, max) {
  return Math.max(min, Math.min(v, max));
}

const styles = StyleSheet.create({
  container: {
    marginVertical: 12,
  },
  title: {
    marginBottom: 15,
  },
  barContainer: {
    width: BAR_WIDTH,
    height: 60,
    position: "relative",
  },
  amPmLabel: {
    position: "absolute",
    top: -14, // place label above bar
    fontSize: 12,
    fontWeight: "bold",
  },
  outerBar: {
    width: BAR_WIDTH,
    height: 20,
    borderRadius: 10,
    borderWidth: 1,
    borderColor: "#ccc",
    overflow: "hidden",
    position: "absolute",
    top: 0,
    left: 0,
  },
  timeBlock: {
    position: "absolute",
    top: 0,
    bottom: 0,
  },
  busySegment: {
    position: "absolute",
    top: 0,
    bottom: 0,
    backgroundColor: "red",
    borderRadius: 10,
  },
  tickLabel: {
    position: "absolute",
    fontSize: 12,
    top: 24,
  },
});
