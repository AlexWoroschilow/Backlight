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
    anchors.centerIn: parent

    style: CircularGaugeStyle {
        needle: Rectangle {
            y: outerRadius * 0.15
            implicitWidth: outerRadius * 0.03
            implicitHeight: outerRadius * 0.9
            antialiasing: true
            color: Qt.rgba(0.66, 0.3, 0, 1)
        }
        
       tickmark: Rectangle {
            implicitWidth: outerRadius * 0.04
            antialiasing: true
            implicitHeight: outerRadius * 0.07
            color: "#0000ff"
       }
        
       minorTickmark: Rectangle {
            implicitWidth: outerRadius * 0.03
            antialiasing: true
            implicitHeight: outerRadius * 0.05
            color: "#ff0000"
       }        
       
      tickmarkLabel:  Text {
            font.pixelSize: Math.max(6, outerRadius * 0.15)
            text: styleData.value
            color: "#000000"
            antialiasing: true
       }       
    }
    
	Behavior on value {
	    NumberAnimation {
	        duration: 1000
	    }
	}    
}