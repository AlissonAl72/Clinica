import static com.kms.katalon.core.checkpoint.CheckpointFactory.findCheckpoint
import static com.kms.katalon.core.testcase.TestCaseFactory.findTestCase
import static com.kms.katalon.core.testdata.TestDataFactory.findTestData
import static com.kms.katalon.core.testobject.ObjectRepository.findTestObject
import static com.kms.katalon.core.testobject.ObjectRepository.findWindowsObject
import com.kms.katalon.core.checkpoint.Checkpoint as Checkpoint
import com.kms.katalon.core.cucumber.keyword.CucumberBuiltinKeywords as CucumberKW
import com.kms.katalon.core.mobile.keyword.MobileBuiltInKeywords as Mobile
import com.kms.katalon.core.model.FailureHandling as FailureHandling
import com.kms.katalon.core.testcase.TestCase as TestCase
import com.kms.katalon.core.testdata.TestData as TestData
import com.kms.katalon.core.testng.keyword.TestNGBuiltinKeywords as TestNGKW
import com.kms.katalon.core.testobject.TestObject as TestObject
import com.kms.katalon.core.webservice.keyword.WSBuiltInKeywords as WS
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.kms.katalon.core.windows.keyword.WindowsBuiltinKeywords as Windows
import internal.GlobalVariable as GlobalVariable
import org.openqa.selenium.Keys as Keys

WebUI.openBrowser('')

WebUI.navigateToUrl('http://127.0.0.1:8000/login/?next=/')

WebUI.setText(findTestObject('Object Repository/Adição de Consulta/Page_Clnica Sade Plena/input_Usurio_username'), 'Alisson')

WebUI.setEncryptedText(findTestObject('Object Repository/Adição de Consulta/Page_Clnica Sade Plena/input_Senha_password'), 
    'iEJD8MEks6psGiKDp3aEow==')

WebUI.click(findTestObject('Object Repository/Adição de Consulta/Page_Clnica Sade Plena/button_Entrar'))

WebUI.click(findTestObject('Object Repository/Adição de Consulta/Page_Clnica Sade Plena/a_Consultas'))

WebUI.click(findTestObject('Object Repository/Adição de Consulta/Page_Clnica Sade Plena/a_Agendar Nova Consulta'))

WebUI.selectOptionByValue(findTestObject('Object Repository/Adição de Consulta/Page_Clnica Sade Plena/select_---------  Luzia de Souza'), 
    '10', true)

WebUI.selectOptionByValue(findTestObject('Object Repository/Adição de Consulta/Page_Clnica Sade Plena/select_---------  Carlos Guimares (Neurocir_2acef9'), 
    '2', true)

WebUI.click(findTestObject('Object Repository/Adição de Consulta/Page_Clnica Sade Plena/button_Salvar'))

