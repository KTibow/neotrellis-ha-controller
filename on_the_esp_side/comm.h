#include "esphome.h"
#define ENTITY_LIST_LENGTH 2

class CommCustomComponent : public Component, public UARTDevice, public CustomAPIDevice
{
public:
    std::string all_statuses[10][2] = {
        {"light.outside_lights", "off"},
        {"light.living_room_lamps", "off"}};
    std::string current_entity = "light.outside_lights";
    CommCustomComponent(UARTComponent *parent) : UARTDevice(parent) {}

    void setup() override
    {
        subscribe_homeassistant_state(&CommCustomComponent::on_entity_changed, "light.outside_lights");
        subscribe_homeassistant_state(&CommCustomComponent::on_entity_changed, "light.living_room_lamps");
    }

    void loop() override
    {
        if (available())
        {
            delay(10);
            String command = readString();
            if (command.charAt(0) == 's')
            {
                ESP_LOGD("custom", "Sending report");
                delay(40);
                for (int i = 0; i < ENTITY_LIST_LENGTH; i++)
                {
                    if (all_statuses[i][0] == current_entity)
                    {
                        print(
                            ("(" +
                             all_statuses[i][1] +
                             "|" +
                             current_entity)
                                .c_str());
                    }
                }
            }
            else if (command.charAt(0) == 't')
            {
                ESP_LOGD("custom", "Toggling entity");
                call_homeassistant_service("homeassistant.toggle", {{"entity_id", current_entity}});
                delay(40);
                print("(toggled");
            }
            else if (command.charAt(0) == 'p')
            {
                ESP_LOGD("custom", "Going to previous entity");
                for (int i = 0; i < ENTITY_LIST_LENGTH; i++)
                {
                    if (all_statuses[i][0] == current_entity)
                    {
                        if (i == 0)
                        {
                            current_entity = all_statuses[ENTITY_LIST_LENGTH - 1][0];
                        }
                        else
                        {
                            current_entity = all_statuses[(i - 1) % ENTITY_LIST_LENGTH][0];
                        }
                        break;
                    }
                }
                delay(40);
                print("(preved");
            }
            else if (command.charAt(0) == 'n')
            {
                ESP_LOGD("custom", "Going to next entity");
                for (int i = 0; i < ENTITY_LIST_LENGTH; i++)
                {
                    if (all_statuses[i][0] == current_entity)
                    {
                        current_entity = all_statuses[(i + 1) % ENTITY_LIST_LENGTH][0];
                        break;
                    }
                }
                delay(40);
                print("(nexted");
            }
            else if (command.charAt(0) == 'b')
            {
                std::string brightness = command.substring(1).c_str();
                ESP_LOGD("custom", "Setting brightness to %s", command.substring(1).c_str());
                call_homeassistant_service("light.turn_on", {{"entity_id", current_entity},
                                                             {"brightness_pct", brightness}});
                print("(set");
            }
            else if (command.charAt(0) == 'c')
            {
                std::string hue = getValue(command.substring(1), ',', 0).c_str();
                std::string sat = getValue(command.substring(1), ',', 1).c_str();
                ESP_LOGD("custom", "Setting color: hue is %s, sat is %s",
                         getValue(command.substring(1), ',', 0).c_str(),
                         getValue(command.substring(1), ',', 1).c_str());
                call_homeassistant_service("script.proxy_color", {{"entity_id", current_entity},
                                                                  {"hue_part", hue},
                                                                  {"sat_part", sat}});
                print("(set");
            }
        }
    }

    void on_entity_changed(std::string entity_id, std::string state)
    {
        for (int i = 0; i < ENTITY_LIST_LENGTH; i++)
        {
            if (all_statuses[i][0] == entity_id)
            {
                all_statuses[i][1] = state;
            }
        }
    }

    String getValue(String data, char separator, int index)
    {
        int found = 0;
        int strIndex[] = {0, -1};
        int maxIndex = data.length() - 1;

        for (int i = 0; i <= maxIndex && found <= index; i++)
        {
            if (data.charAt(i) == separator || i == maxIndex)
            {
                found++;
                strIndex[0] = strIndex[1] + 1;
                strIndex[1] = (i == maxIndex) ? i + 1 : i;
            }
        }
        return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
    }
};
