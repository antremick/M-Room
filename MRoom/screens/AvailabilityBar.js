import React, { useMemo, useRef, useEffect } from "react";
import { View, Text, StyleSheet, ScrollView } from "react-native";

// Adjust these to define the timeline range in 24-hr format
const START_HOUR_24 = 8; // 8:00 AM
const END_HOUR_24 = 23; // 11:00 PM

export default function AvailabilityBar({ room }) {
  const scrollRef = useRef(null);

  // Build half-hour slots from START_HOUR_24 to END_HOUR_24
  const slots = useMemo(() => {
    const result = [];
    let hour = START_HOUR_24;
    let min = 0;
    while (true) {
      result.push({ hour24: hour, minute: min });
      min += 30;
      if (min >= 60) {
        min = 0;
        hour = (hour + 1) % 24;
      }
      if (hour === END_HOUR_24 && min === 0) {
        break;
      }
    }
    return result;
  }, []);

  const CELL_WIDTH = 65;

  // On mount, scroll to the current time (floored to nearest half-hour)
  useEffect(() => {
    if (!scrollRef.current) return;

    const now = new Date();
    let hour24 = now.getHours();
    let minute = now.getMinutes();
    minute = minute < 30 ? 0 : 30;

    let index = 0;
    for (let i = 0; i < slots.length; i++) {
      const slot = slots[i];
      if (
        timeToAbsoluteMinutes(slot.hour24, slot.minute) >=
        timeToAbsoluteMinutes(hour24, minute)
      ) {
        index = i;
        break;
      }
    }
    scrollRef.current.scrollTo({
      x: index * CELL_WIDTH,
      y: 0,
      animated: false,
    });
  }, [slots]);

  return (
    <View style={styles.container}>
      <Text style={styles.roomTitle}>{room.roomNum}</Text>
      <ScrollView horizontal ref={scrollRef} showsHorizontalScrollIndicator>
        <View style={{ flexDirection: "row" }}>
          {slots.map((slot, i) => {
            const label = formatSlot(slot.hour24, slot.minute);
            // Mark slot red if it overlaps any meeting's start-end range
            const inMeeting = isSlotInMeeting(
              room.meetings,
              slot.hour24,
              slot.minute
            );
            return (
              <View
                key={i}
                style={[
                  styles.slotCell,
                  {
                    backgroundColor: inMeeting ? "red" : "green",
                    width: CELL_WIDTH,
                  },
                ]}
              >
                <Text style={styles.slotText}>{label}</Text>
              </View>
            );
          })}
        </View>
      </ScrollView>
    </View>
  );
}

/**
 * Check if the half-hour slot (hour24, minute) is within any meeting's range.
 * If a meeting ends at 9:00 PM, the slot starting at 9:00 PM is green
 * (since end time is exclusive).
 */
function isSlotInMeeting(meetings, hour24, min) {
  const slotMin = timeToAbsoluteMinutes(hour24, min);
  return meetings.some((mtg) => {
    const startMin = parseTimeToMinutes(mtg.MtgStartTime);
    const endMin = parseTimeToMinutes(mtg.MtgEndTime);
    // Occupied if slotMin >= start && slotMin < end
    return slotMin >= startMin && slotMin < endMin;
  });
}

/** Convert hour24 + minute -> absolute minutes in [0..1439]. */
function timeToAbsoluteMinutes(h24, m) {
  return h24 * 60 + m;
}

/**
 * Parse times like "9:00 PM" -> 1260 (21*60).
 * Adjust to your actual meeting times format as needed.
 */
function parseTimeToMinutes(str) {
  const [timePart, ampm] = str.split(" ");
  const [hh, mm] = timePart.split(":");
  let hour = parseInt(hh, 10) % 12;
  let minute = parseInt(mm, 10) || 0;
  if (ampm.toUpperCase() === "PM") hour += 12;
  return hour * 60 + minute;
}

/** Format hour24,minute => e.g. "9:30 PM" or "10 AM". */
function formatSlot(hour24, minute) {
  let h = hour24 % 12;
  if (h === 0) h = 12;
  const ampm = hour24 < 12 ? "AM" : "PM";
  if (minute === 0) return `${h} ${ampm}`;
  return `${h}:${minute < 10 ? "0" : ""}${minute} ${ampm}`;
}

const styles = StyleSheet.create({
  container: {
    marginVertical: 8,
  },
  roomTitle: {
    fontWeight: "bold",
    marginBottom: 4,
  },
  slotCell: {
    height: 40,
    justifyContent: "center",
    alignItems: "center",
    marginRight: 2,
  },
  slotText: {
    color: "#fff",
    fontWeight: "600",
  },
});
