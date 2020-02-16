namespace WinEEPROM
{
    partial class Form1
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.lstPort = new System.Windows.Forms.CheckedListBox();
            this.btnReadAll = new System.Windows.Forms.Button();
            this.txtAddressBits = new System.Windows.Forms.TextBox();
            this.label1 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.label5 = new System.Windows.Forms.Label();
            this.txtReadAddress = new System.Windows.Forms.TextBox();
            this.label6 = new System.Windows.Forms.Label();
            this.btnReadAddress = new System.Windows.Forms.Button();
            this.btnWriteAddress = new System.Windows.Forms.Button();
            this.label7 = new System.Windows.Forms.Label();
            this.txtWriteData = new System.Windows.Forms.TextBox();
            this.txtWriteAddress = new System.Windows.Forms.TextBox();
            this.label4 = new System.Windows.Forms.Label();
            this.label8 = new System.Windows.Forms.Label();
            this.viwData = new System.Windows.Forms.ListView();
            this.Address = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.Data0 = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.Data1 = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.Data2 = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.Data3 = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.Data4 = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.Data5 = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.Data6 = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.Data7 = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.Data8 = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.Data9 = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.Char0 = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.Char1 = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.Char2 = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.Char3 = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.Char4 = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.Char5 = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.Char6 = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.Char7 = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.Char8 = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.Char9 = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.label9 = new System.Windows.Forms.Label();
            this.txtBaudRate = new System.Windows.Forms.TextBox();
            this.label10 = new System.Windows.Forms.Label();
            this.lblStatus = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // lstPort
            // 
            this.lstPort.FormattingEnabled = true;
            this.lstPort.Location = new System.Drawing.Point(12, 25);
            this.lstPort.Name = "lstPort";
            this.lstPort.Size = new System.Drawing.Size(120, 79);
            this.lstPort.TabIndex = 2;
            this.lstPort.SelectedIndexChanged += new System.EventHandler(this.lstPort_SelectedIndexChanged);
            // 
            // btnReadAll
            // 
            this.btnReadAll.Location = new System.Drawing.Point(12, 215);
            this.btnReadAll.Name = "btnReadAll";
            this.btnReadAll.Size = new System.Drawing.Size(75, 23);
            this.btnReadAll.TabIndex = 5;
            this.btnReadAll.Text = "Read all";
            this.btnReadAll.UseVisualStyleBackColor = true;
            this.btnReadAll.Click += new System.EventHandler(this.btnReadAll_Click);
            // 
            // txtAddressBits
            // 
            this.txtAddressBits.Location = new System.Drawing.Point(12, 165);
            this.txtAddressBits.Name = "txtAddressBits";
            this.txtAddressBits.Size = new System.Drawing.Size(100, 20);
            this.txtAddressBits.TabIndex = 7;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(12, 9);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(85, 13);
            this.label1.TabIndex = 8;
            this.label1.Text = "Select COM port";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(155, 9);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(77, 13);
            this.label2.TabIndex = 9;
            this.label2.Text = "EEPROM data";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(12, 149);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(64, 13);
            this.label3.TabIndex = 10;
            this.label3.Text = "Address bits";
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(12, 199);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(105, 13);
            this.label5.TabIndex = 12;
            this.label5.Text = "Read from EEPROM";
            // 
            // txtReadAddress
            // 
            this.txtReadAddress.Location = new System.Drawing.Point(12, 257);
            this.txtReadAddress.Name = "txtReadAddress";
            this.txtReadAddress.Size = new System.Drawing.Size(100, 20);
            this.txtReadAddress.TabIndex = 13;
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Location = new System.Drawing.Point(9, 241);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(45, 13);
            this.label6.TabIndex = 14;
            this.label6.Text = "Address";
            // 
            // btnReadAddress
            // 
            this.btnReadAddress.Location = new System.Drawing.Point(12, 283);
            this.btnReadAddress.Name = "btnReadAddress";
            this.btnReadAddress.Size = new System.Drawing.Size(75, 23);
            this.btnReadAddress.TabIndex = 15;
            this.btnReadAddress.Text = "Read address";
            this.btnReadAddress.UseVisualStyleBackColor = true;
            // 
            // btnWriteAddress
            // 
            this.btnWriteAddress.Location = new System.Drawing.Point(12, 425);
            this.btnWriteAddress.Name = "btnWriteAddress";
            this.btnWriteAddress.Size = new System.Drawing.Size(75, 23);
            this.btnWriteAddress.TabIndex = 18;
            this.btnWriteAddress.Text = "Write";
            this.btnWriteAddress.UseVisualStyleBackColor = true;
            // 
            // label7
            // 
            this.label7.AutoSize = true;
            this.label7.Location = new System.Drawing.Point(9, 322);
            this.label7.Name = "label7";
            this.label7.Size = new System.Drawing.Size(84, 13);
            this.label7.TabIndex = 17;
            this.label7.Text = "Write to address";
            // 
            // txtWriteData
            // 
            this.txtWriteData.Location = new System.Drawing.Point(12, 399);
            this.txtWriteData.Name = "txtWriteData";
            this.txtWriteData.Size = new System.Drawing.Size(100, 20);
            this.txtWriteData.TabIndex = 16;
            // 
            // txtWriteAddress
            // 
            this.txtWriteAddress.Location = new System.Drawing.Point(12, 360);
            this.txtWriteAddress.Name = "txtWriteAddress";
            this.txtWriteAddress.Size = new System.Drawing.Size(100, 20);
            this.txtWriteAddress.TabIndex = 19;
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(9, 344);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(45, 13);
            this.label4.TabIndex = 20;
            this.label4.Text = "Address";
            // 
            // label8
            // 
            this.label8.AutoSize = true;
            this.label8.Location = new System.Drawing.Point(12, 383);
            this.label8.Name = "label8";
            this.label8.Size = new System.Drawing.Size(30, 13);
            this.label8.TabIndex = 21;
            this.label8.Text = "Data";
            // 
            // viwData
            // 
            this.viwData.Columns.AddRange(new System.Windows.Forms.ColumnHeader[] {
            this.Address,
            this.Data0,
            this.Data1,
            this.Data2,
            this.Data3,
            this.Data4,
            this.Data5,
            this.Data6,
            this.Data7,
            this.Data8,
            this.Data9,
            this.Char0,
            this.Char1,
            this.Char2,
            this.Char3,
            this.Char4,
            this.Char5,
            this.Char6,
            this.Char7,
            this.Char8,
            this.Char9});
            this.viwData.HideSelection = false;
            this.viwData.Location = new System.Drawing.Point(158, 25);
            this.viwData.Name = "viwData";
            this.viwData.Size = new System.Drawing.Size(630, 423);
            this.viwData.TabIndex = 22;
            this.viwData.UseCompatibleStateImageBehavior = false;
            // 
            // label9
            // 
            this.label9.AutoSize = true;
            this.label9.Location = new System.Drawing.Point(12, 110);
            this.label9.Name = "label9";
            this.label9.Size = new System.Drawing.Size(55, 13);
            this.label9.TabIndex = 24;
            this.label9.Text = "BaudRate";
            // 
            // txtBaudRate
            // 
            this.txtBaudRate.Location = new System.Drawing.Point(12, 126);
            this.txtBaudRate.Name = "txtBaudRate";
            this.txtBaudRate.Size = new System.Drawing.Size(100, 20);
            this.txtBaudRate.TabIndex = 23;
            this.txtBaudRate.TextChanged += new System.EventHandler(this.txtBaudRate_TextChanged);
            // 
            // label10
            // 
            this.label10.AutoSize = true;
            this.label10.Location = new System.Drawing.Point(618, 9);
            this.label10.Name = "label10";
            this.label10.Size = new System.Drawing.Size(40, 13);
            this.label10.TabIndex = 25;
            this.label10.Text = "Status:";
            // 
            // lblStatus
            // 
            this.lblStatus.AutoSize = true;
            this.lblStatus.Location = new System.Drawing.Point(665, 9);
            this.lblStatus.Name = "lblStatus";
            this.lblStatus.Size = new System.Drawing.Size(41, 13);
            this.lblStatus.TabIndex = 26;
            this.lblStatus.Text = "label11";
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(800, 457);
            this.Controls.Add(this.lblStatus);
            this.Controls.Add(this.label10);
            this.Controls.Add(this.label9);
            this.Controls.Add(this.txtBaudRate);
            this.Controls.Add(this.viwData);
            this.Controls.Add(this.label8);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.txtWriteAddress);
            this.Controls.Add(this.btnWriteAddress);
            this.Controls.Add(this.label7);
            this.Controls.Add(this.txtWriteData);
            this.Controls.Add(this.btnReadAddress);
            this.Controls.Add(this.label6);
            this.Controls.Add(this.txtReadAddress);
            this.Controls.Add(this.label5);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.txtAddressBits);
            this.Controls.Add(this.btnReadAll);
            this.Controls.Add(this.lstPort);
            this.Name = "Form1";
            this.Text = "EEPROM Programmer";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion
        private System.Windows.Forms.CheckedListBox lstPort;
        private System.Windows.Forms.Button btnReadAll;
        private System.Windows.Forms.TextBox txtAddressBits;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.TextBox txtReadAddress;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.Button btnReadAddress;
        private System.Windows.Forms.Button btnWriteAddress;
        private System.Windows.Forms.Label label7;
        private System.Windows.Forms.TextBox txtWriteData;
        private System.Windows.Forms.TextBox txtWriteAddress;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Label label8;
        private System.Windows.Forms.ListView viwData;
        private System.Windows.Forms.ColumnHeader Address;
        private System.Windows.Forms.ColumnHeader Data0;
        private System.Windows.Forms.ColumnHeader Data1;
        private System.Windows.Forms.ColumnHeader Data2;
        private System.Windows.Forms.ColumnHeader Data3;
        private System.Windows.Forms.ColumnHeader Data4;
        private System.Windows.Forms.ColumnHeader Data5;
        private System.Windows.Forms.ColumnHeader Data6;
        private System.Windows.Forms.ColumnHeader Data7;
        private System.Windows.Forms.ColumnHeader Data8;
        private System.Windows.Forms.ColumnHeader Data9;
        private System.Windows.Forms.ColumnHeader Char0;
        private System.Windows.Forms.ColumnHeader Char1;
        private System.Windows.Forms.ColumnHeader Char2;
        private System.Windows.Forms.ColumnHeader Char3;
        private System.Windows.Forms.ColumnHeader Char4;
        private System.Windows.Forms.ColumnHeader Char5;
        private System.Windows.Forms.ColumnHeader Char6;
        private System.Windows.Forms.ColumnHeader Char7;
        private System.Windows.Forms.ColumnHeader Char8;
        private System.Windows.Forms.ColumnHeader Char9;
        private System.Windows.Forms.Label label9;
        private System.Windows.Forms.TextBox txtBaudRate;
        private System.Windows.Forms.Label label10;
        private System.Windows.Forms.Label lblStatus;
    }
}

