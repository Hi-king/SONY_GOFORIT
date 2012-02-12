#include <string>
#include <list>
#include <vector>
#include <iostream>
#include <ctime>

const char* DOC = "\
============================================================== \n\
 q3_fast                                                       \n\
-------------------------------------------------------------- \n\
 arguments                                                     \n\
    |- (1.targetstring)                                        \n\
        |- default : sony                                      \n\
    |- (2.codestring)                                          \n\
        |- default : from problem                              \n\
 output                                                        \n\
    |- skip[0],index[0]\n .... skip[n],index[n]\n              \n\
    |- time= $(hour):$(minute):$(second)                       \n\
 example                                                       \n\
    |- $ q3_fast                                               \n\
    |- $ q3_fast sony ssoonnyy                                 \n\
-------------------------------------------------------------  \n\
 for Python 2.7                                                \n\
 K.Ogaki(ogaki@iis.u-tokyo.ac.jp)                              \n\
 2012/02/12                                                    \n\
-------------------------------------------------------------  \n\
 This program is released under GPL.                           \n\
 http://www.opensource.jp/gpl/gpl.ja.html.euc-jp               \n\
=============================================================  \n\
\
";
/*
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

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
	for(long long i = 0; i<300000; i++){
		codestr += ( 0x61 + ( 26 * ( r / 0x10000) ) / 0x10000); 
		r = ( r*1103515245 + 12345 ) & ( 0xFFFFFFFF );
	}
	return codestr;
}

/* -----------
   search
------------ */
std::list<std::vector<long long> > search1(const std::string& code, const std::string& target){
	std::list<long long> list1;
	std::list<long long> listlast;

	std::list<std::vector<long long> > anslist;

	for(long long i = 0; i<code.size(); i++){
		if(code[i] == target[0]){
			list1.push_back(i);
		}
		else if(code[i] == target[target.size()-1]){
			listlast.push_back(i);
		}
	}

	const int skiptime = target.size()-1;

	for(std::list<long long>::iterator it1 = list1.begin(); it1 != list1.end(); it1++){

		for(std::list<long long>::iterator itlast = listlast.begin(); itlast != listlast.end(); itlast++){

            if( (*itlast-*it1) % skiptime  != 0)continue;//枝刈り
            long long skip = (*itlast-*it1)/skiptime;
			
			/* check */
			int nowi=1;
			for(long long now = *it1+skip; nowi<skiptime;now+=skip,nowi++){
              
              if(code[now]!=target[nowi])break;
			}

			/* anslist */
			if( nowi==(skiptime) ){
                std::vector<long long> nowans(2);
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


int main(int argc, char** argv){
    std::string targetstr = "sony";
    if(argc>1)targetstr = argv[1];

    std::string codestr = "";
    if(argc>2){
        codestr = argv[2];
    }
    else{
        codestr = codegen();
    }


	std::clock_t s = std::clock();
	std::list<std::vector<long long> > anslist = search1(codestr, targetstr);
    anslist.sort();
	std::clock_t e = std::clock();

    for(std::list<std::vector<long long> >::iterator it = anslist.begin(); it != anslist.end(); it++){
      std::cout<<(*it)[0]<<","<<(*it)[1]<<std::endl;
    }

	std::cout<<"time="<<(double)(e-s)/CLOCKS_PER_SEC<<std::endl;
	std::cout<<"ansnum="<<anslist.size()<<std::endl;

}
