# service.py
import win32serviceutil
import win32service
import win32event
import servicemanager
import sys
import os
from pathlib import Path
import threading
import logging

# Add the service directory to Python path
SERVICE_DIR = os.path.dirname(os.path.abspath(__file__))
if SERVICE_DIR not in sys.path:
    sys.path.insert(0, SERVICE_DIR)

from server import app  # Import after adding to path

class YTTranscriberService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'YTTranscriberService'
    _svc_display_name_ = 'YouTube Transcriber Service'
    _svc_description_ = 'Provides YouTube video transcription and summarization services'
    
    _exe_name_ = sys.executable
    _exe_args_ = f'"{os.path.abspath(__file__)}"'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.run_server_flag = True

        # Set up logging
        log_dir = Path(r'C:\ProgramData\YTTranscriber\logs')
        log_dir.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            filename=str(log_dir / 'service.log'),
            level=logging.DEBUG,
            format='%(asctime)s - %(message)s'
        )
        logging.info('Service initialized')
        logging.info(f'Service directory: {SERVICE_DIR}')
        logging.info(f'Python path: {sys.path}')

    def SvcStop(self):
        """Stop the service"""
        logging.info('Stop signal received')
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.run_server_flag = False
        win32event.SetEvent(self.stop_event)

    def SvcDoRun(self):
        """Start the service"""
        try:
            logging.info('Service is starting...')
            self.ReportServiceStatus(win32service.SERVICE_RUNNING)
            
            # Start Flask in a separate thread
            server_thread = threading.Thread(target=self.run_flask)
            server_thread.daemon = True
            server_thread.start()
            
            logging.info('Server thread started')
            
            # Wait for stop event
            while self.run_server_flag:
                if win32event.WaitForSingleObject(self.stop_event, 1000) == win32event.WAIT_OBJECT_0:
                    break
            
            logging.info('Service stopped')
                
        except Exception as e:
            logging.error(f'Service error: {str(e)}')
            self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def run_flask(self):
        """Run the Flask application"""
        try:
            app.run(host='0.0.0.0', port=5000)
        except Exception as e:
            logging.error(f'Flask error: {str(e)}')

if __name__ == '__main__':
    if len(sys.argv) == 1:
        try:
            servicemanager.Initialize()
            servicemanager.PrepareToHostSingle(YTTranscriberService)
            servicemanager.StartServiceCtrlDispatcher()
        except Exception as e:
            logging.error(f'Service failed to start: {str(e)}')
            raise
    else:
        win32serviceutil.HandleCommandLine(YTTranscriberService)