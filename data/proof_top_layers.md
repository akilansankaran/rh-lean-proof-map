# Top of the proof tree (from Main.lean)

## depth 0 (5 declarations)

- **LFunction_eq_zero_re** (theorem, `Main`, 2 lines)
  `theorem LFunction_eq_zero_re : DirichletLZerosOnLine`
- **LFunction_eq_zero_re_of_isPrimitive** (theorem, `Main`, 2 lines)
  `theorem LFunction_eq_zero_re_of_isPrimitive : PrimitiveDirichletLZerosOnLine`
- **LFunction_ne_zero_of_half_lt_re** (theorem, `Main`, 2 lines)
  `theorem LFunction_ne_zero_of_half_lt_re : DirichletLNonvanishingRightOfHalf`
- **riemannHypothesis** (theorem, `Main`, 2 lines)
  `theorem riemannHypothesis : RiemannHypothesis`
- **riemannZeta_eq_zero_re** (theorem, `Main`, 2 lines)
  `theorem riemannZeta_eq_zero_re : RiemannZetaZerosOnLine`

## depth 1 (7 declarations)

- **DirichletLNonvanishingRightOfHalf** (def, `Statements`, 4 lines)
  `def DirichletLNonvanishingRightOfHalf : Prop`
- **DirichletLZerosOnLine** (def, `Statements`, 4 lines)
  `def DirichletLZerosOnLine : Prop`
- **PrimitiveDirichletLZerosOnLine** (def, `Statements`, 4 lines)
  `def PrimitiveDirichletLZerosOnLine : Prop`
- **RiemannZetaZerosOnLine** (def, `Statements`, 3 lines)
  `def RiemannZetaZerosOnLine : Prop`
- **allChi** (theorem, `Supplements.Kernels.MainTheorems`, 2 lines)
  `theorem allChi : UpperTheory.EveryCharacter`
- **critAll** (theorem, `Supplements.Kernels.MainTheorems`, 4 lines)
  `theorem critAll (N : ℕ) [NeZero N] (χ : DirichletCharacter ℂ N) (hχ : χ.IsPrimitive) (s : ℂ) (h0 : 0 < s.re) (h1 : s.re < 1) (hz : LFunction χ s = 0) : s.re = 1 / 2`
- **rhOfAll** (theorem, `Supplements.Kernels.MainTheorems`, 2 lines)
  `theorem rhOfAll : RiemannHypothesis`

## depth 2 (4 declarations)

- **Formalism.VW.critLine** (theorem, `Formalism.GammaFactorNonvanishing.CritLine`, 18 lines)
  `theorem Formalism.VW.critLine (h : UpperTheory.EveryCharacter) (N : ℕ) [NeZero N] (χ : DirichletCharacter ℂ N) (hχ : χ.IsPrimitive) (s : ℂ) (h0 : 0 < s.re) (h1 : s.re < 1) (hz : LFunction χ s = 0) : s.re = 1 / 2`
- **Formalism.VW.rh_of_every** (theorem, `Formalism.GammaFactorNonvanishing.CritLine`, 5 lines)
  `theorem Formalism.VW.rh_of_every (h : UpperTheory.EveryCharacter) : RiemannHypothesis`
- **UpperTheory.EveryCharacter** (def, `Development.AutomorphicArithmetic.CharacterBoxes.EveryCharacter`, 3 lines)
  `def UpperTheory.EveryCharacter : Prop`
- **UpperTheory.FinalTheorems.everyCharacter** (theorem, `Development.AutomorphicArithmetic.CharacterBoxes.MainConclusion`, 3 lines)
  `theorem UpperTheory.FinalTheorems.everyCharacter : UpperTheory.EveryCharacter`

## depth 3 (4 declarations)

- **Formalism.VW.gammaFactor_ne_zero** (theorem, `Formalism.GammaFactorNonvanishing.CritLine`, 5 lines)
  `theorem Formalism.VW.gammaFactor_ne_zero {N : ℕ} (χ : DirichletCharacter ℂ N) {s : ℂ} (hs : 0 < s.re) : gammaFactor χ s ≠ 0`
- **Formalism.VW.rh_of_right** (theorem, `Formalism.GammaFactorNonvanishing.RhOfRight`, 59 lines)
  `theorem Formalism.VW.rh_of_right (hz : ∀ s : ℂ, 1 / 2 < s.re → s ≠ 1 → riemannZeta s ≠ 0) : RiemannHypothesis`
- **UpperTheory.FinalTheorems.everyCharacter_of_row** (theorem, `Development.AutomorphicArithmetic.CharacterBoxes.MainConclusion`, 3 lines)
  `theorem UpperTheory.FinalTheorems.everyCharacter_of_row (h : UpperTheory.GalStar.Row0b fun h rc => UpperTheory.Zero.LLC.IsRecT h rc) : UpperTheory.EveryCharacter`
- **UpperTheory.Gal.Int.galoisLocalGlobalStrong_recParameter** (theorem, `Development.AutomorphicArithmetic.Foundations.GaloisRepresentations.IntegralStructures.RowSrc`, 4 lines)
  `theorem galoisLocalGlobalStrong_recParameter : UpperTheory.GalStar.Row0b recT`

## depth 4 (9 declarations)

- **UpperTheory.Gal.Int.galoisRepresentations_of_thetaLift** (theorem, `Development.AutomorphicArithmetic.Foundations.GaloisRepresentations.IntegralStructures.GaloisRepresentationsOfThetaLift`, 4 lines)
  `theorem galoisRepresentations_of_thetaLift (up : UpperTheory.TP.TLiftK) : UpperTheory.GalStar.Row0b recT`
- **UpperTheory.Gal.Int.recT** (def, `Development.AutomorphicArithmetic.Foundations.GaloisRepresentations.IntegralStructures.Development`, 2 lines)
  `def recT : UpperTheory.GalStar.RecNotion`
- **UpperTheory.GalStar.Row0b** (def, `Development.AutomorphicArithmetic.Foundations.GaloisRepresentations.TypeConditions.WeightsConjBis`, 6 lines)
  `def Row0b : Prop`
- **UpperTheory.LiteratureTheorems.every_character_of_literature_of_vWin** (theorem, `Development.AutomorphicArithmetic.ThetaCorrespondence.ThetaPairLifts.ThirdPlaceSeries.EveryCharacterOfLiteratureOfVWin`, 6 lines)
  `theorem UpperTheory.LiteratureTheorems.every_character_of_literature_of_vWin (O : _root_.UpperTheory.LiteratureTheorems.OpenLiteratureStatements) (hV : UpperTheory.Top.VWin) : UpperTheory.EveryCharacter`
- **UpperTheory.One.vwin_of_row** (theorem, `Development.AutomorphicArithmetic.AutomorphicVarieties.ModularityArgument.ThresholdArguments.DenseThresholdCases.VwinOfRow`, 3 lines)
  `theorem UpperTheory.One.vwin_of_row (h : UpperTheory.GalStar.Row0b fun h rc => UpperTheory.Zero.LLC.IsRecT h rc) : UpperTheory.Top.VWin`
- **UpperTheory.TP.K.tLiftK** (theorem, `Development.AutomorphicArithmetic.Foundations.GaloisRepresentations.ThetaParseval.ThetaKernels.TLiftK`, 3 lines)
  `theorem UpperTheory.TP.K.tLiftK : UpperTheory.TP.TLiftK`
- **UpperTheory.Zero.LLC.IsRecT** (def, `Development.AutomorphicArithmetic.Foundations.LocalLanglands.IsRecTOfIsRec`, 2 lines)
  `def IsRecT (rc : IrrGL (w.adicCompletion E) → WD h) : Prop`
- **UpperTheory.Zero.LLC.recTExists** (theorem, `Development.AutomorphicArithmetic.Foundations.LocalLanglands.LocalCentralUnits.RecTExists`, 48 lines)
  `theorem UpperTheory.Zero.LLC.recTExists : UpperTheory.Zero.LLC.RecTExists`
- **key** (lemma, `Development.AutomorphicArithmetic.IntegralCasts.CapelliIdentities.GaloisBoundSecond`, 119 lines)
  `private lemma key {F : Type} [Field F] [NumberField F] [NumberField.IsTotallyReal F] (N : ℕ) (hN : 0 < N) (I : Ideal (RingOfIntegers F)) (hI : I ≠ ⊥) (B : ℝ) (hB : 0 ≤ B) (S : Set F) (hS : S = {x : F | x ≠ 0 ∧ (∃ y ∈ I, (y : F) = (N : F) * x) ∧ ∀ w : InfinitePlace F, (w : F → ℝ) x ≤ B}) : S.Finite ∧ (S.ncard : ℝ) * (Ideal.absNorm I : ℝ) ≤ (4 * B * N) ^ Module.finrank ℚ F`

