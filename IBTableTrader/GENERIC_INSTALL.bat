for /F %%A in ('dir ..\..\..\..\..\Anaconda /AD /S /B') do ( 
	call "%%A\Scripts\activate.bat"
	(echo call "%%A\Scripts\activate.bat" & echo voila ./src/OptionRangeTrader.ipynb & echo PAUSE)>GENERICRUN.bat
)
pip install yfinance
pip install ib_insync
pip install voila
PAUSE