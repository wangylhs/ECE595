package data_frame;

import java.io.*;
import java.sql.*;
import java.text.DecimalFormat;
import java.util.*;

public class Trace_Predict {
	static Connection connection;
	public static Properties props;
	
	public static void readProperties() throws IOException {
		props = new Properties();
		FileInputStream in = new FileInputStream("database.properties");
		props.load(in);
		in.close();
	}
	
	public static void openConnection() throws SQLException, IOException
	{
		String drivers = props.getProperty("jdbc.drivers");
		if (drivers != null) System.setProperty("jdbc.drivers", drivers);

		String url = props.getProperty("jdbc.url");
		String username = props.getProperty("jdbc.username");
		String password = props.getProperty("jdbc.password");

		connection = DriverManager.getConnection( url, username, password);
	}
	
	public static void get_target_data(String web, String day, String time) 
			throws SQLException, IOException{
		Statement stat = connection.createStatement();
		ResultSet result = stat.executeQuery("SELECT * FROM ecn_data WHERE dest='"+web+"' and time like '"
				+day+"%"+time+":%'");
		String[] tc = new String[700];
		Integer[] ct = new Integer[700];
		String temp="";
		String delay="";
		String[] s;
		String[] tc_delay = new String[700];
		String[] d;
		String[] d_old;
		int current_index=0;
		Arrays.fill(ct,1);
		while(result.next()){
			for(int i=0;i<21;i++){
				s=result.getString(i+2).split(" ");
				if(s.length==2){
					temp += s[0]+" ";
					delay += s[1]+" ";
				}else{
					temp += s[0]+" ";
				}
			}
			for(int i=0;i<700;i++){
				if(tc[i]!=null && tc[i].contains(temp)){
					ct[i]++;
					d_old = tc_delay[i].split(" ");
					d=delay.split(" ");
					tc_delay[i]="";
					for(int j=0;j<d.length;j++){
						double v = (Double.parseDouble(d_old[j])+Double.parseDouble(d[j]))/2;
						d[j] = new DecimalFormat("####.##").format(v);
						tc_delay[i]+=d[j]+" ";
					}
					temp="";
					delay="";
					break;
				}else if(i==699){
					//System.out.println(current_index);
					tc[current_index]=temp;
					tc_delay[current_index]=delay;
					current_index++;
					temp="";
					delay="";
				}
			}
			
			//System.out.println(result.getString(2));
			
		}
		int max=ct[0];
		for(int i=0;i<700;i++){
			if(ct[i]>max) max=ct[i];
		}
		//System.out.println(max);
		for(int i=0;i<700;i++){
			if(tc[i]!=null && ct[i]==max){
				s=tc[i].split(" ");
				d=tc_delay[i].split(" ");
				System.out.println(s[0]);
				for(int j=0;j<d.length;j++){
					System.out.println(j+1 + " "+ s[j+1]+" "+d[j]);
				}
			}
		}
		
		
		
		
	}
	
	public static void main(String[] args) throws SQLException, IOException{
		@SuppressWarnings("resource")
		Scanner scanner = new Scanner( System.in );
		System.out.print( "web name(xxx.xxx.xxx): " );
		String web = scanner.nextLine();
		System.out.print( "Input a Day(Mon-Fri): " );
		String day = scanner.nextLine();
		System.out.print( "Input a time(hour): " );
		String time = scanner.nextLine();
		readProperties();
		openConnection();
		get_target_data(web,day,time);
	}
}
