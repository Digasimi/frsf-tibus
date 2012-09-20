package frsf.tibus.util;

public abstract class SplashScreen {
	static String header = 			"\n\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n";
	static String bodyStarting =  	" Starting TibusServer \n";
	static String bodyStarted =  	" TibusServer Succesfully Started \n";
	static String footer = 			"++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n";
	
	public SplashScreen()
	{
		
	}
	
	public static String getStartingSplashScreen()
	{
		return header + bodyStarting + footer;
	}
	
	public static String getStartedSplashScreen()
	{
		return header + bodyStarted + footer;
	}
}
