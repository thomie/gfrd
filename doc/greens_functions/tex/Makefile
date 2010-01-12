# Todo. Use that Makefile.am magic. And why is it recompiling even though 
# nothing changed?

# make should produce:
#   * 1 pdf for the derivation of the Greens function of each diffusion 
#   problem. (Todo)
#   * 1 pdf for each problem giving the results: Greens function, survival 
#   probability and propensity function.
#   * greensFunctions.pdf, all results combined.


PDFLATEX=pdflatex -output-directory=../build

greensFunctions.pdf: greensFunctions.tex greensFunction1DAbsAbs.pdf greensFunction1DAbsInf.pdf greensFunction1DRadAbs.pdf greensFunction1DRadInf.pdf greensFunction2DNoneAbs.pdf greensFunction2DRadInf.pdf greensFunction2DRadAbs.pdf greensFunction3DNoneAbs.pdf greensFunction3DRadInf.pdf greensFunction3DRadAbs.pdf
	$(PDFLATEX) greensFunctions.tex

greensFunction1DAbsAbs.pdf: greensFunction1DAbsAbs.tex include/greensFunction1DAbsAbs.include.tex include/greensFunction1DAbsAbsDerivation.include.tex 
	$(PDFLATEX) greensFunction1DAbsAbs.tex 

greensFunction1DAbsInf.pdf: greensFunction1DAbsInf.tex include/greensFunction1DAbsInf.include.tex include/greensFunction1DAbsInfDerivation.include.tex
	$(PDFLATEX) greensFunction1DAbsInf.tex

greensFunction1DRadAbs.pdf: greensFunction1DRadAbs.tex include/greensFunction1DRadAbs.include.tex include/greensFunction1DRadAbsDerivation.include.tex
	$(PDFLATEX) greensFunction1DRadAbs.tex

greensFunction1DRadInf.pdf: greensFunction1DRadInf.tex include/greensFunction1DRadInf.include.tex include/greensFunction1DRadInfDerivation.include.tex
	$(PDFLATEX) greensFunction1DRadInf.tex

greensFunction2DNoneAbs.pdf: greensFunction2DNoneAbs.tex include/greensFunction2DNoneAbs.include.tex include/greensFunction2DNoneAbsDerivation.include.tex
	$(PDFLATEX) greensFunction2DNoneAbs.tex

greensFunction2DRadInf.pdf: greensFunction2DRadInf.tex include/greensFunction2DRadInf.include.tex include/greensFunction2DRadInfDerivation.include.tex
	$(PDFLATEX) greensFunction2DRadInf.tex

greensFunction2DRadAbs.pdf: greensFunction2DRadAbs.tex include/greensFunction2DRadAbs.include.tex include/greensFunction2DRadAbsDerivation.include.tex
	$(PDFLATEX) greensFunction2DRadAbs.tex

greensFunction3DNoneAbs.pdf: greensFunction3DNoneAbs.tex include/greensFunction3DNoneAbs.include.tex include/greensFunction3DNoneAbsDerivation.include.tex
	$(PDFLATEX) greensFunction3DNoneAbs.tex

greensFunction3DRadInf.pdf: greensFunction3DRadInf.tex include/greensFunction3DRadInf.include.tex include/greensFunction3DRadInfDerivation.include.tex
	$(PDFLATEX) greensFunction3DRadInf.tex

greensFunction3DRadAbs.pdf: greensFunction3DRadAbs.tex include/greensFunction3DRadAbs.include.tex include/greensFunction3DRadAbsDerivation.include.tex
	$(PDFLATEX) greensFunction3DRadAbs.tex

