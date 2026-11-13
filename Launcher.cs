using System;
using System.Diagnostics;
using System.IO;
using System.Net;
using System.Threading;

namespace PowerGuardLauncher
{
    class Program
    {
        [STAThread]
        static void Main(string[] args)
        {
            string appDir = AppDomain.CurrentDomain.BaseDirectory.TrimEnd('\\', '/');
            string url = "http://localhost:8501";

            // If already responding, just open browser and exit
            if (IsServerAlive(url))
            {
                OpenBrowser(url);
                return;
            }

            // Find python or streamlit executable
            string pythonPath = FindPythonExecutable();
            string command = "streamlit run dashboard.py";
            string fileName = "cmd.exe";
            string arguments = "/c " + command;

            if (!string.IsNullOrEmpty(pythonPath))
            {
                // Run directly via python -m streamlit to be 100% reliable across environments
                arguments = string.Format("/c \"\"{0}\" -m streamlit run dashboard.py\"", pythonPath);
            }

            ProcessStartInfo psi = new ProcessStartInfo
            {
                FileName = fileName,
                Arguments = arguments,
                WorkingDirectory = appDir,
                CreateNoWindow = true,
                UseShellExecute = false,
                WindowStyle = ProcessWindowStyle.Hidden
            };

            Process serverProcess = null;
            try
            {
                serverProcess = Process.Start(psi);
            }
            catch (Exception ex)
            {
                // In case of error, show a standard Windows message box
                System.Windows.Forms.MessageBox.Show(
                    "Error launching PowerGuard AI dashboard:\n" + ex.Message,
                    "PowerGuard AI Error",
                    System.Windows.Forms.MessageBoxButtons.OK,
                    System.Windows.Forms.MessageBoxIcon.Error
                );
                return;
            }

            // Wait for Streamlit to start responding on port 8501 (up to 15 seconds)
            bool ready = false;
            for (int i = 0; i < 30; i++)
            {
                Thread.Sleep(500);
                if (IsServerAlive(url))
                {
                    ready = true;
                    break;
                }
            }

            // Open the browser automatically
            OpenBrowser(url);

            // Keep the background server process alive
            if (serverProcess != null && !serverProcess.HasExited)
            {
                serverProcess.WaitForExit();
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
            try
            {
                Process.Start(new ProcessStartInfo(url) { UseShellExecute = true });
            }
            catch
            {
                try
                {
                    Process.Start("cmd.exe", "/c start " + url);
                }
                catch { }
            }
        }

        static string FindPythonExecutable()
        {
            // Check common paths
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

            // Fallback to "python.exe" on PATH
            return "python.exe";
        }
    }
}

