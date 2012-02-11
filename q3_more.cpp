#include <string>
#include <list>
#include <iostream>
#include <ctime>

/*
compile
/Zi /nologo /W3 /WX- /O2 /Oi /Oy- /GL /D "_MBCS" /Gm- /EHsc /GS /Gy /fp:precise /Zc:wchar_t /Zc:forScope /Fd"Release\vc100.pdb" /Gd /analyze- /errorReport:queue
*/


/* ---------------------
  code generation
----------------------- */
std::string codegen(){
	long long r = 16;
	std::string codestr = "";
	for(long long i = 0; i<=300000; i++){
		codestr += ( 0x61 + ( 26 * ( r / 0x10000) ) / 0x10000); 
		r = ( r*1103515245 + 12345 ) & ( 0xFFFFFFFF );
	}
	return codestr;
}


/* -----------
   search
------------ */
std::list<long long*> search1(const std::string& code, const std::string& target){
	std::list<long long> list1;
	std::list<long long> listlast;

	std::list<long long*> anslist;

	for(long long i = 0; i<code.size(); i++){
		if(code[i] == target[0]){
			list1.push_back(i);
		}
		else if(code[i] == target[target.size()-1]){
			listlast.push_back(i);
		}
	}

	const int skiptime = target.size()-1;

	long long now = 0;
	for(std::list<long long>::iterator it1 = list1.begin(); it1 != list1.end(); it1++){
		//std::cout<<"\r"<<now*100.0/list1.size();
		now++;

		for(std::list<long long>::iterator itlast = listlast.begin(); itlast != listlast.end(); itlast++){

			if((*itlast-*it1)%skiptime != 0) continue;
			
			/* check */
			int nowi=1;
			for(long long now = *it1+(*itlast-*it1); nowi<skiptime; nowi++, now+=(*itlast-*it1)){
				if(code[now]!=target[nowi])break;
			}

			/* anslist */
			if( nowi==(skiptime-1) ){
				long long nowans[2];
				if(*it1<*itlast){
					nowans[0] = (*itlast-*it1)/skiptime;
					nowans[1] = *it1;
				}
				else{
					nowans[0] = (*it1 - *itlast)/skiptime;
					nowans[1] = *itlast;
				}
				anslist.push_back(nowans); 
			}
		}
	}

	return anslist;
}


int main(){
	std::string code = codegen();
	std::cout<<code[208728]<<code[208728+4162]<<code[208728+4162*2]<<code[208728+4162*3]<<std::endl;

	std::clock_t s = std::clock();
	std::list<long long*> anslist = search1(code, "sony");
	std::clock_t e = std::clock();

	std::cout<<std::endl;
	std::cout<<"time="<<(double)(e-s)/CLOCKS_PER_SEC<<std::endl;
	std::cout<<"ansnum="<<anslist.size()<<std::endl;

	int a;
	std::cin>>a;
}