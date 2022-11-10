# test_reaction_annotation.py
# Test for ReactionAnnotation class

import libsbml
import numpy as np
import os
import sys
import unittest

from AMAS import species_annotation as sa
from AMAS import reaction_annotation as ra
from AMAS import constants as cn
from AMAS import tools


E_COLI_PATH = os.path.join(cn.TEST_DIR, 'e_coli_core.xml')
BIOMD_248_PATH = os.path.join(cn.TEST_DIR, 'BIOMD0000000248.xml')
# ID of a reaction
R_PFK = 'R_PFK'
ATP = 'M_atp_c'
COMPONENTS = {'M_fdp_c', 'M_adp_c', 'M_atp_c', 'M_f6p_c', 'M_h_c'}
ONE_CANDIDATE = 'RHEA:12423'
ONE_CHEBI = 'CHEBI:30616'

# Dummy data for calculating accuracy, recalll & precision
DUMMY_REF = {'a': ['ABC', 'BCD'],
              'b': ['DEF']}
DUMMY_PRED = {'a': ['ABC'],
             'b': ['AAA']}


#############################
# Tests
#############################
class TestReactionAnnotation(unittest.TestCase):

  def setUp(self):
    self.spec_cl = sa.SpeciesAnnotation(libsbml_fpath = E_COLI_PATH)
    self.reac_cl = ra.ReactionAnnotation(libsbml_fpath = E_COLI_PATH)
    pred_species = self.spec_cl.predictAnnotationByName(inp_spec_list=COMPONENTS)
    self.pred_reaction = self.reac_cl.predictAnnotation(inp_spec_dict=self.spec_cl.formula,
                                                        inp_reac_list=[R_PFK],
                                                        update=True)
  ### Was used for iteration algorithm
  # def testGetMatchScore(self):
  #   one_dict = {'R1': {'M1': 0.7}}
  #   one_match_score = self.reac_cl.getMatchScore(score_dict=one_dict)
  #   self.assertEqual(one_match_score, 0.7)

  def testGetReactionComponents(self):
    # When argument is string, i.e., reaction ID
    one_comps = self.reac_cl.getReactionComponents(R_PFK)
    self.assertEqual(COMPONENTS, set(one_comps))
    # When argument is a libsbml.Reaction instance
    one_r = self.reac_cl.model.getReaction(R_PFK)
    two_comps = self.reac_cl.getReactionComponents(one_r)
    self.assertEqual(COMPONENTS, set(two_comps))

  def testPredictAnnotation(self):
    match_scores_dict = self.pred_reaction[cn.MATCH_SCORE]
    self.assertTrue(ONE_CANDIDATE in [val[0] for val in match_scores_dict[R_PFK]])
    self.assertTrue(0.8 in [val[1] for val in match_scores_dict[R_PFK]])

  def testEvaluatePredictedReactionAnnotation(self):
    one_eval = self.reac_cl.evaluatePredictedReactionAnnotation(inp_dict=self.pred_reaction)
    self.assertEqual(np.round(one_eval[R_PFK],2), 0.91)


# Probably unncessary
  # def testGetBestOneCandidates(self):
  #   # When argument is directly given
  #   one_match_score = {'R1': [('RHEA:1', 1.0), ('RHEA:2', 0.5)]}
  #   self.assertEqual(self.reac_cl.getBestOneCandidates(one_match_score)['R1'],
  #                    ['RHEA:1'])
  #   # When argument is not given
  #   self.assertEqual(self.reac_cl.getBestOneCandidates()[R_PFK],
  #                    [ONE_CANDIDATE])

  ### Was used for iteration algorithm
  # def testUpdateSpeciesByAReaction(self):
  #   chebi2update = self.reac_cl.updateSpeciesByAReaction(inp_rid=R_PFK,
  #                                                        inp_spec_dict=self.spec_cl.formula,
  #                                                        inp_rhea=ONE_CANDIDATE)
  #   self.assertEqual(chebi2update[ATP], [ONE_CHEBI])

  def testGetAccuracy(self):
    pred = {R_PFK: ['RHEA:16112']}
    self.assertEqual(self.reac_cl.getAccuracy(pred_annotation=pred), 1.0)


  def testGetRecall(self):
    recall1 = self.reac_cl.getRecall(ref_annotation=DUMMY_REF,
                                     pred_annotation=DUMMY_PRED,
                                     mean=True)
    self.assertEqual(recall1, 0.25)
    recall2 = self.reac_cl.getRecall(pred_annotation=self.pred_reaction[cn.CANDIDATES])
    self.assertEqual(recall2, 1.0)


  def testGetPrecision(self):
    precision1 = self.reac_cl.getPrecision(ref_annotation=DUMMY_REF,
                                           pred_annotation=DUMMY_PRED,
                                           mean=True)
    self.assertEqual(precision1, 0.5)
    precision2 = self.reac_cl.getPrecision(pred_annotation=self.pred_reaction[cn.CANDIDATES])
    self.assertEqual(np.round(precision2, 2), 0.17)











