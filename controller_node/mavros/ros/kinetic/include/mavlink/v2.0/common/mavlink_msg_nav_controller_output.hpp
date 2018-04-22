// MESSAGE NAV_CONTROLLER_OUTPUT support class

#pragma once

namespace mavlink {
namespace common {
namespace msg {

/**
 * @brief NAV_CONTROLLER_OUTPUT message
 *
 * The state of the fixed wing navigation and position controller.
 */
struct NAV_CONTROLLER_OUTPUT : mavlink::Message {
    static constexpr msgid_t MSG_ID = 62;
    static constexpr size_t LENGTH = 26;
    static constexpr size_t MIN_LENGTH = 26;
    static constexpr uint8_t CRC_EXTRA = 183;
    static constexpr auto NAME = "NAV_CONTROLLER_OUTPUT";


    float nav_roll; /*< Current desired roll in degrees */
    float nav_pitch; /*< Current desired pitch in degrees */
    int16_t nav_bearing; /*< Current desired heading in degrees */
    int16_t target_bearing; /*< Bearing to current MISSION/target in degrees */
    uint16_t wp_dist; /*< Distance to active MISSION in meters */
    float alt_error; /*< Current altitude error in meters */
    float aspd_error; /*< Current airspeed error in meters/second */
    float xtrack_error; /*< Current crosstrack error on x-y plane in meters */


    inline std::string get_name(void) const override
    {
            return NAME;
    }

    inline Info get_message_info(void) const override
    {
            return { MSG_ID, LENGTH, MIN_LENGTH, CRC_EXTRA };
    }

    inline std::string to_yaml(void) const override
    {
        std::stringstream ss;

        ss << NAME << ":" << std::endl;
        ss << "  nav_roll: " << nav_roll << std::endl;
        ss << "  nav_pitch: " << nav_pitch << std::endl;
        ss << "  nav_bearing: " << nav_bearing << std::endl;
        ss << "  target_bearing: " << target_bearing << std::endl;
        ss << "  wp_dist: " << wp_dist << std::endl;
        ss << "  alt_error: " << alt_error << std::endl;
        ss << "  aspd_error: " << aspd_error << std::endl;
        ss << "  xtrack_error: " << xtrack_error << std::endl;

        return ss.str();
    }

    inline void serialize(mavlink::MsgMap &map) const override
    {
        map.reset(MSG_ID, LENGTH);

        map << nav_roll;                      // offset: 0
        map << nav_pitch;                     // offset: 4
        map << alt_error;                     // offset: 8
        map << aspd_error;                    // offset: 12
        map << xtrack_error;                  // offset: 16
        map << nav_bearing;                   // offset: 20
        map << target_bearing;                // offset: 22
        map << wp_dist;                       // offset: 24
    }

    inline void deserialize(mavlink::MsgMap &map) override
    {
        map >> nav_roll;                      // offset: 0
        map >> nav_pitch;                     // offset: 4
        map >> alt_error;                     // offset: 8
        map >> aspd_error;                    // offset: 12
        map >> xtrack_error;                  // offset: 16
        map >> nav_bearing;                   // offset: 20
        map >> target_bearing;                // offset: 22
        map >> wp_dist;                       // offset: 24
    }
};

} // namespace msg
} // namespace common
} // namespace mavlink
