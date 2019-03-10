import QtQuick 2.0
import QtQuick.Controls 1.4
import QtQuick.Controls.Styles 1.4
import QtQuick.Extras 1.4
import QtQuick.Extras.Private 1.0

CircularGauge {
    property real gauge_value: 0.0
    objectName: "test_gauge"
    minimumValue: 0
    value: gauge_value
    maximumValue: 100
    
    style: CircularGaugeStyle {
		minimumValueAngle: -90
		maximumValueAngle: 90
        needle: Rectangle {
            y: outerRadius * 0.15
            implicitWidth: outerRadius * 0.03
            implicitHeight: outerRadius * 0.9
            antialiasing: true
            color: Qt.rgba(0.66, 0.3, 0, 1)
        }
    }
    
      Behavior on value {
          NumberAnimation {
              duration: 1000
          }
      }    
}