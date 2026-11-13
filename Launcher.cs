using System;
using System.Diagnostics;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.IO;
using System.Net;
using System.Threading;
using System.Windows.Forms;

namespace PowerGuardLauncher
{
    public class SplashForm : Form
    {
        private ProgressBar progressBar;
        private Label statusLabel;
        private Image logoImage;

        public SplashForm()
        {
            this.FormBorderStyle = FormBorderStyle.None;
            this.StartPosition = FormStartPosition.CenterScreen;
            this.Size = new Size(440, 280);
            this.BackColor = Color.FromArgb(11, 15, 25);
            this.TopMost = true;
            this.ShowInTaskbar = true;
            this.DoubleBuffered = true;

            // Load logo if present
            string logoPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "Logo.PNG");
            if (File.Exists(logoPath))
            {
                try
                {
                    using (var bmp = new Bitmap(logoPath))
                    {
                        logoImage = new Bitmap(bmp);
                    }
                }
                catch { }
            }

            // Title Label
            Label titleLabel = new Label
            {
                Text = "POWERGUARD AI",
                Font = new Font("Segoe UI", 16, FontStyle.Bold),
                ForeColor = Color.FromArgb(248, 250, 252),
                TextAlign = ContentAlignment.MiddleCenter,
                Size = new Size(400, 32),
                Location = new Point(20, 105)
            };
            this.Controls.Add(titleLabel);

            // Subtitle
            Label subLabel = new Label
            {
                Text = "Next-Gen Electrical Diagnostics Platform",
                Font = new Font("Segoe UI", 9.5f, FontStyle.Regular),
                ForeColor = Color.FromArgb(148, 163, 184),
                TextAlign = ContentAlignment.MiddleCenter,
                Size = new Size(400, 22),
                Location = new Point(20, 138)
            };
            this.Controls.Add(subLabel);

            // Status message
            statusLabel = new Label
            {
                Text = "Initializing diagnostic engine & AI models...",
                Font = new Font("Segoe UI", 9f, FontStyle.Regular),
                ForeColor = Color.FromArgb(56, 189, 248),
                TextAlign = ContentAlignment.MiddleCenter,
                Size = new Size(400, 20),
                Location = new Point(20, 195)
            };
            this.Controls.Add(statusLabel);

            // Marquee Progress Bar
            progressBar = new ProgressBar
            {
                Style = ProgressBarStyle.Marquee,
                MarqueeAnimationSpeed = 30,
                Size = new Size(340, 8),
                Location = new Point(50, 175)
            };
            this.Controls.Add(progressBar);
        }

        public void SetStatus(string text)
        {
            if (this.InvokeRequired)
            {
                this.BeginInvoke(new Action<string>(SetStatus), text);
                return;
            }
            statusLabel.Text = text;
        }

        protected override void OnPaint(PaintEventArgs e)
        {
            base.OnPaint(e);
            Graphics g = e.Graphics;
            g.SmoothingMode = SmoothingMode.AntiAlias;

            // Draw Subtle Outer Border
            using (Pen borderPen = new Pen(Color.FromArgb(56, 189, 248), 2))
            {
                g.DrawRectangle(borderPen, 1, 1, this.Width - 2, this.Height - 2);
            }

            // Draw Logo or Icon
            if (logoImage != null)
            {
                int logoSize = 64;
                int logoX = (this.Width - logoSize) / 2;
                int logoY = 28;

                // Draw subtle glowing background for logo
                using (SolidBrush glowBrush = new SolidBrush(Color.FromArgb(20, 56, 189, 248)))
                {
                    g.FillEllipse(glowBrush, logoX - 6, logoY - 6, logoSize + 12, logoSize + 12);
                }
                using (Pen glowPen = new Pen(Color.FromArgb(50, 56, 189, 248), 1))
                {
                    g.DrawEllipse(glowPen, logoX - 6, logoY - 6, logoSize + 12, logoSize + 12);
                }

                g.DrawImage(logoImage, logoX, logoY, logoSize, logoSize);
            }
            else
            {
                // Fallback text icon
                using (Font iconFont = new Font("Segoe UI", 28, FontStyle.Bold))
                using (Brush iconBrush = new SolidBrush(Color.FromArgb(56, 189, 248)))
                {
                    string iconText = "⚡";
                    SizeF sz = g.MeasureString(iconText, iconFont);
                    g.DrawString(iconText, iconFont, iconBrush, (this.Width - sz.Width) / 2, 28);
                }
            }
        }
    }

    class Program
    {
        [STAThread]
        static void Main(string[] args)
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);

            SplashForm splash = new SplashForm();

            // Run backend server launch on separate thread
            Thread worker = new Thread(() =>
            {
                RunLauncherWorkflow(splash);
            });
            worker.IsBackground = true;
            worker.Start();

            Application.Run(splash);
        }

        static void RunLauncherWorkflow(SplashForm splash)
        {
            string appDir = AppDomain.CurrentDomain.BaseDirectory.TrimEnd('\\', '/');
            string url = "http://localhost:8501";

            try
            {
                // 1. Check if server is already running
                if (IsServerAlive(url))
                {
                    splash.SetStatus("Server already running. Opening dashboard...");
                    Thread.Sleep(600);
                    OpenBrowser(url);
                    CloseSplash(splash);
                    return;
                }

                // 2. Locate Python / Streamlit executable
                splash.SetStatus("Starting PowerGuard background engine...");
                string pythonPath = FindPythonExecutable();
                string arguments = string.Format("/c \"\"{0}\" -m streamlit run dashboard.py\"", pythonPath);

                ProcessStartInfo psi = new ProcessStartInfo
                {
                    FileName = "cmd.exe",
                    Arguments = arguments,
                    WorkingDirectory = appDir,
                    CreateNoWindow = true,
                    UseShellExecute = false,
                    WindowStyle = ProcessWindowStyle.Hidden
                };

                Process.Start(psi);

                // 3. Poll server until HTTP 200 is returned
                splash.SetStatus("Loading neural baselines & telemetry...");
                int maxAttempts = 40; // 40 * 350ms = ~14 seconds

                for (int i = 0; i < maxAttempts; i++)
                {
                    Thread.Sleep(350);
                    if (IsServerAlive(url))
                    {
                        break;
                    }
                    if (i == 10)
                    {
                        splash.SetStatus("Starting Streamlit web service...");
                    }
                    else if (i == 20)
                    {
                        splash.SetStatus("Finalizing connection to localhost:8501...");
                    }
                }

                splash.SetStatus("Connected! Opening browser...");
                Thread.Sleep(500);

                // 4. Open default browser
                OpenBrowser(url);
                Thread.Sleep(300);

                // 5. Close splash loader
                CloseSplash(splash);
            }
            catch (Exception ex)
            {
                splash.SetStatus("Error: " + ex.Message);
                Thread.Sleep(2000);
                CloseSplash(splash);
            }
        }

        static void CloseSplash(SplashForm splash)
        {
            if (splash.InvokeRequired)
            {
                splash.BeginInvoke(new Action(() => splash.Close()));
            }
            else
            {
                splash.Close();
            }
        }

        static bool IsServerAlive(string url)
        {
            try
            {
                HttpWebRequest request = (HttpWebRequest)WebRequest.Create(url);
                request.Method = "GET";
                request.Timeout = 1000;
                using (HttpWebResponse response = (HttpWebResponse)request.GetResponse())
                {
                    return response.StatusCode == HttpStatusCode.OK;
                }
            }
            catch
            {
                return false;
            }
        }

        static void OpenBrowser(string url)
        {
            // Try browsers in order: Chrome → Edge (tab mode) → Firefox → explorer fallback
            // Always use --new-tab / -new-tab to open inside the browser, NOT in app/standalone mode

            string[] chromePaths = new string[]
            {
                @"C:\Program Files\Google\Chrome\Application\chrome.exe",
                @"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
                    @"Google\Chrome\Application\chrome.exe")
            };

            string[] edgePaths = new string[]
            {
                @"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                @"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
            };

            string[] firefoxPaths = new string[]
            {
                @"C:\Program Files\Mozilla Firefox\firefox.exe",
                @"C:\Program Files (x86)\Mozilla Firefox\firefox.exe"
            };

            // 1. Try Chrome (--new-tab opens a real browser tab)
            foreach (string chrome in chromePaths)
            {
                if (File.Exists(chrome))
                {
                    Process.Start(new ProcessStartInfo
                    {
                        FileName = chrome,
                        Arguments = "--new-tab " + url,
                        UseShellExecute = false
                    });
                    return;
                }
            }

            // 2. Try Edge with --new-tab (NOT app mode)
            foreach (string edge in edgePaths)
            {
                if (File.Exists(edge))
                {
                    Process.Start(new ProcessStartInfo
                    {
                        FileName = edge,
                        Arguments = "--new-tab " + url,
                        UseShellExecute = false
                    });
                    return;
                }
            }

            // 3. Try Firefox
            foreach (string ff in firefoxPaths)
            {
                if (File.Exists(ff))
                {
                    Process.Start(new ProcessStartInfo
                    {
                        FileName = ff,
                        Arguments = "-new-tab " + url,
                        UseShellExecute = false
                    });
                    return;
                }
            }

            // 4. Final fallback: explorer.exe (always opens default browser in normal window)
            try
            {
                Process.Start(new ProcessStartInfo("explorer.exe", url)
                {
                    UseShellExecute = false
                });
            }
            catch { }
        }

        static string FindPythonExecutable()
        {
            string localApp = Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData);
            string[] testPaths = new string[]
            {
                Path.Combine(localApp, @"Programs\Python\Python313\python.exe"),
                Path.Combine(localApp, @"Programs\Python\Python312\python.exe"),
                Path.Combine(localApp, @"Programs\Python\Python311\python.exe"),
                Path.Combine(localApp, @"Programs\Python\Python310\python.exe"),
                @"C:\Python313\python.exe",
                @"C:\Python312\python.exe",
                @"C:\Python311\python.exe",
                @"C:\Python310\python.exe"
            };

            foreach (string p in testPaths)
            {
                if (File.Exists(p)) return p;
            }

            return "python.exe";
        }
    }
}
