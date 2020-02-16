using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO.Ports;

namespace WinEEPROM
{
    public partial class Form1 : Form
    {
        static SerialPort _serialPort;

        public Form1()
        {
            InitializeComponent();
            lblStatus.Text = "Select COM port...";
            // Get a list of serial port names.
            string[] ports = SerialPort.GetPortNames();
            // Display each port name to the console.
            lstPort.Items.Clear();
            foreach (string port in ports)
            {
                lstPort.Items.Add(port);
            }
        }

        private void lstPort_SelectedIndexChanged(object sender, EventArgs e)
        {
            // Create a new SerialPort object with default settings.
            _serialPort = new SerialPort();
            // Allow the user to set the appropriate properties.
            string port = lstPort.CheckedItems.ToString();
            MessageBox.Show(port);
            if (port != "")
            {
                _serialPort.PortName = port;
            } else
            {
                lblStatus.Text = "Select COM port...";
                return;
            }
            
            Int32 baudRate;
            Int32.TryParse(txtBaudRate.ToString(), out baudRate);
            if (baudRate != -1 && baudRate != 0)
            {
                _serialPort.BaudRate = baudRate;
            } else
            {
                lblStatus.Text = "Set baud rate...";
                return;
            }
            //_serialPort.Parity = SetPortParity(_serialPort.Parity);
            //_serialPort.DataBits = SetPortDataBits(_serialPort.DataBits);
            //_serialPort.StopBits = SetPortStopBits(_serialPort.StopBits);
        }

        private void txtBaudRate_TextChanged(object sender, EventArgs e)
        {
            Int32 baudRate;
            Int32.TryParse(txtBaudRate.ToString(), out baudRate);
            if (baudRate != -1 && baudRate != 0)
            {
                _serialPort.BaudRate = baudRate;
            }
            else
            {
                lblStatus.Text = "Set baud rate...";
            }
        }

        private void btnReadAll_Click(object sender, EventArgs e)
        {

        }

    }
}
