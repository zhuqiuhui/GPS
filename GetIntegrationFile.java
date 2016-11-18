package preprocess;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

public class GetIntegrationFile {
	static String nonMode = "none";
	public static void getIntegrationFile(String labelFilePath, String pointsFilePath, String writeFilePath) throws IOException{
		List<String> labelLines = Files.readAllLines(Paths.get(labelFilePath));
		List<String> pointsLines = Files.readAllLines(Paths.get(pointsFilePath));
		List<String> writeContents = new ArrayList<String>();
		
		int pointLineNum = 1;
		for(String l:pointsLines){
			System.out.println(pointLineNum);
			String[] pointArr = l.split(",");
			String timeStamp = pointArr[5]+" "+pointArr[6];
			String temp = pointArr[0]+","+pointArr[1]+","+timeStamp+",";
			
			int find = 0;
			for(int i = 1;i<labelLines.size();i++){
				String[] lineArr = labelLines.get(i).split("	");
				String startStr = lineArr[0]+" "+lineArr[1];
				String endStr = lineArr[0]+" "+lineArr[2];
				if(isInTime1(startStr, endStr, timeStamp)==1){
					temp = temp + lineArr[3];
					find = 1;
					break;
				} // if
			} // for
			if(find==0)
				temp = temp + nonMode;
			writeContents.add(temp);
			pointLineNum++;
		} // for
		// start to write file!
		File wfile = new File(writeFilePath);
		if(!wfile.exists()){
			wfile.createNewFile();
		}
		BufferedWriter bw = new BufferedWriter(new FileWriter(wfile, true));
		for(String wline: writeContents){
			bw.write(wline+"\r\n");
		} // for
		bw.close();
	}

	public static int isInTime1(String time1, String time2, String time3){
		/*
		 * 如果time3在time1~time2范围之内，返回1，否则返回0
		 */
		int f1 = isInTime2(time1, time3);
		int f2 = isInTime2(time2, time3);
		if(f1==1&&f2==0)
			return 1;
		else
			return 0;
	}
	
	public static int isInTime2(String time1, String time2){
		/*
		 * 如果time1在time2之前返回1，否则返回0
		 */
		SimpleDateFormat sdf = new SimpleDateFormat("yyyy/MM/dd HH:mm:ss");
		Date d1;
		Date d2;
		int flag = 0;
		try {
			d1 = sdf.parse(time1);
			d2 = sdf.parse(time2);
			if(d1.before(d2))
				flag = 1;
		} catch (ParseException e) {
			e.printStackTrace();
		}
		return flag;
	}
	
	public static void main(String[] args) throws Exception {
		String commonPath = "E:\\【学习】\\【学术论文】\\【学位论文】\\实验部分\\data\\";
		String rPath = commonPath + "integration\\";
		String wPath = commonPath + "integration_process\\";
		for(int i = 1;i<=32;i++){
			System.out.println("Processing "+i+" th file......");
			String num = String.valueOf(i);
			String labelFilePath = rPath + "labels_" + num +".txt";
			String pointsFilePath = rPath + "integration_" + num +".txt";
			String writeFilePath = wPath + "integration_" + num +".txt";
			getIntegrationFile(labelFilePath, pointsFilePath, writeFilePath);
		}// for
	}

}
