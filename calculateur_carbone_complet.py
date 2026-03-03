import streamlit as st
import pandas as pd

# Configuration CSS pour le design moderne
st.markdown("""
<style>
.main-header {
    text-align: center;
    background: linear-gradient(90deg, #1e3c72, #2a5298);
    padding: 2rem;
    border-radius: 15px;
    color: white;
    margin-bottom: 2rem;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    border: 2px solid rgba(255, 255, 255, 0.1);
}

.main-header h1 {
    margin: 0;
    font-size: 2.8rem;
    font-weight: 700;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.main-header p {
    margin: 0.5rem 0 0 0;
    opacity: 0.95;
    font-size: 1.2rem;
}

.constituant-box {
    border: 2px solid #e1e5e9;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    background: linear-gradient(135deg, #f8f9fa, #e9ecef);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.metric-card {
    background: white;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    text-align: center;
    border-left: 4px solid #007bff;
}

.scope-header {
    background: linear-gradient(90deg, #28a745, #20c997);
    color: white;
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 1rem;
    text-align: center;
    font-weight: 600;
}

.result-box {
    background: linear-gradient(135deg, #007bff, #0056b3);
    color: white;
    padding: 1.5rem;
    border-radius: 12px;
    margin: 1rem 0;
    text-align: center;
    box-shadow: 0 6px 12px rgba(0, 123, 255, 0.3);
}

.export-section {
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 10px;
    border: 2px dashed #007bff;
    margin-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# Header principal avec toutes les informations
st.markdown("""
<div class="main-header">
    <h1>🌍 Calculateur d'Empreinte Carbone</h1>
    <p>Analyse complète des émissions de CO₂ par constituant</p>
    <p style="font-size: 1.0rem; opacity: 0.9; margin-top: 1rem;">
        <strong>École Nationale des Ingénieurs de Monastir</strong>
    </p>
    <p style="font-size: 0.9rem; opacity: 0.8; margin-top: 0.5rem;">
        TPE combustion / Halima Bouajina , Nermine Dardouri , Arwa khemira , Rima Yeferni , Ons Selmi
    </p>
</div>
""", unsafe_allow_html=True)

# Section de configuration principale
st.sidebar.markdown("## ⚙️ Configuration du Projet")
produit_final = st.sidebar.text_input("📦 Nom du produit final", placeholder="Ex: Smartphone, Voiture, etc.")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔧 Nombre de Constituants")
nb_constituants = st.sidebar.number_input("Nombre de constituants", min_value=1, max_value=15, value=3, step=1)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Mode d'analyse")
mode_analyse = st.sidebar.selectbox(
    "Choisissez le mode d'analyse",
    ["🧩 Analyse par constituants", "📈 Analyse globale par scopes"]
)

st.divider()

# Stockage des données
constituants_data = []
total_general = 0

if mode_analyse == "🧩 Analyse par constituants":
    st.markdown("## 🧩 Analyse Détaillée par Constituants")
    st.markdown("*Analysez chaque composant individuellement puis obtenez l'empreinte carbone totale de l'assemblage*")
    
    # Interface pour chaque constituant
    for i in range(nb_constituants):
        with st.expander(f"🧩 Constituant {i+1}", expanded=True if i < 2 else False):
            col_nom, col_poids = st.columns([2, 1])
            
            with col_nom:
                nom_constituant = st.text_input(f"📝 Nom du constituant {i+1}", 
                                             placeholder=f"Ex: Batterie, Écran, Moteur...", 
                                             key=f"nom_{i}")
            
            with col_poids:
                poids_constituant = st.number_input(f"⚖️ Poids (kg)", min_value=0.0, value=1.0, key=f"poids_{i}")
            
            # Scope 1 pour ce constituant
            st.markdown('<div class="scope-header">🟦 Scope 1 - Émissions Directes</div>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📊 Quantités**")
                diesel_q = st.number_input(f"🛢️ Diesel – quantité (L)", min_value=0.0, value=0.0, key=f"diesel_q_{i}")
                gaz_q = st.number_input(f"🔥 Gaz naturel – quantité (m³)", min_value=0.0, value=0.0, key=f"gaz_q_{i}")
                ess_q = st.number_input(f"⛽ Essence – quantité (L)", min_value=0.0, value=0.0, key=f"ess_q_{i}")
            
            with col2:
                st.markdown("**🔢 Facteurs d'émission**")
                diesel_f = st.number_input(f"🛢️ Diesel – facteur (kg CO₂/L)", min_value=0.0, value=2.68, key=f"diesel_f_{i}")
                gaz_f = st.number_input(f"🔥 Gaz naturel – facteur (kg CO₂/m³)", min_value=0.0, value=2.02, key=f"gaz_f_{i}")
                ess_f = st.number_input(f"⛽ Essence – facteur (kg CO₂/L)", min_value=0.0, value=2.31, key=f"ess_f_{i}")
            
            # Scope 2 pour ce constituant
            st.markdown('<div class="scope-header">🟨 Scope 2 - Électricité</div>', unsafe_allow_html=True)
            col3, col4 = st.columns(2)
            
            with col3:
                kwh = st.number_input(f"⚡ Consommation électrique (kWh)", min_value=0.0, value=0.0, key=f"kwh_{i}")
            
            with col4:
                fact_elec = st.number_input(f"⚡ Facteur électricité (kg CO₂/kWh)", min_value=0.0, value=0.059, key=f"fact_elec_{i}")
            
            # Scope 3 pour ce constituant
            st.markdown('<div class="scope-header">🟧 Scope 3 - Autres Émissions</div>', unsafe_allow_html=True)
            col5, col6 = st.columns(2)
            
            with col5:
                st.markdown("**📊 Quantités**")
                trans_q = st.number_input(f"🚚 Transport – quantité (km)", min_value=0.0, value=0.0, key=f"trans_q_{i}")
                mat_q = st.number_input(f"🏭 Matières premières – quantité (kg)", min_value=0.0, value=0.0, key=f"mat_q_{i}")
                dech_q = st.number_input(f"🗑️ Déchets – quantité (kg)", min_value=0.0, value=0.0, key=f"dech_q_{i}")
            
            with col6:
                st.markdown("**🔢 Facteurs d'émission**")
                trans_f = st.number_input(f"🚚 Transport – facteur (kg CO₂/km)", min_value=0.0, value=0.12, key=f"trans_f_{i}")
                mat_f = st.number_input(f"🏭 Matières premières – facteur (kg CO₂/kg)", min_value=0.0, value=1.5, key=f"mat_f_{i}")
                dech_f = st.number_input(f"🗑️ Déchets – facteur (kg CO₂/kg)", min_value=0.0, value=0.8, key=f"dech_f_{i}")
            
            # Calculs pour ce constituant
            scope1_constituant = diesel_q * diesel_f + gaz_q * gaz_f + ess_q * ess_f
            scope2_constituant = kwh * fact_elec
            scope3_constituant = trans_q * trans_f + mat_q * mat_f + dech_q * dech_f
            total_constituant = scope1_constituant + scope2_constituant + scope3_constituant
            
            # Affichage des résultats pour ce constituant
            st.markdown("---")
            st.markdown(f"### 📊 Résultats pour {nom_constituant if nom_constituant else f'Constituant {i+1}'}")
            
            col_result1, col_result2, col_result3, col_result4 = st.columns(4)
            
            with col_result1:
                st.markdown(f'<div class="metric-card"><h4>🟦 Scope 1</h4><h3>{scope1_constituant:.2f}</h3><p>kg CO₂</p></div>', unsafe_allow_html=True)
            
            with col_result2:
                st.markdown(f'<div class="metric-card"><h4>🟨 Scope 2</h4><h3>{scope2_constituant:.2f}</h3><p>kg CO₂</p></div>', unsafe_allow_html=True)
            
            with col_result3:
                st.markdown(f'<div class="metric-card"><h4>🟧 Scope 3</h4><h3>{scope3_constituant:.2f}</h3><p>kg CO₂</p></div>', unsafe_allow_html=True)
            
            with col_result4:
                st.markdown(f'<div class="metric-card" style="border-left-color: #28a745;"><h4>🎯 Total</h4><h3>{total_constituant:.2f}</h3><p>kg CO₂</p></div>', unsafe_allow_html=True)
            
            # Stocker les données
            constituants_data.append({
                'Constituant': nom_constituant if nom_constituant else f"Constituant {i+1}",
                'Poids (kg)': poids_constituant,
                'Scope 1 (kg CO₂)': scope1_constituant,
                'Scope 2 (kg CO₂)': scope2_constituant,
                'Scope 3 (kg CO₂)': scope3_constituant,
                'Total (kg CO₂)': total_constituant
            })
            
            total_general += total_constituant

else:  # Mode analyse globale
    st.markdown("## 📈 Analyse Globale par Scopes")
    st.markdown("*Analysez l'empreinte carbone globale du produit par scopes*")
    
    # Scope 1 - Émissions directes
    with st.expander("🟦 Scope 1 – Émissions directes", expanded=True):
        st.markdown("**Émissions directes provenant de sources possédées ou contrôlées**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📊 Quantités**")
            diesel_q = st.number_input("🛢️ Diesel – quantité (L)", min_value=0.0, value=0.0)
            gaz_q = st.number_input("🔥 Gaz naturel – quantité (m³)", min_value=0.0, value=0.0)
            ess_q = st.number_input("⛽ Essence – quantité (L)", min_value=0.0, value=0.0)
        
        with col2:
            st.markdown("**🔢 Facteurs d'émission**")
            diesel_f = st.number_input("🛢️ Diesel – facteur (kg CO₂/L)", min_value=0.0, value=2.68)
            gaz_f = st.number_input("🔥 Gaz naturel – facteur (kg CO₂/m³)", min_value=0.0, value=2.02)
            ess_f = st.number_input("⛽ Essence – facteur (kg CO₂/L)", min_value=0.0, value=2.31)
        
        # Calculs Scope 1
        diesel_e = diesel_q * diesel_f
        gaz_e = gaz_q * gaz_f
        ess_e = ess_q * ess_f
        
        scope1 = diesel_e + gaz_e + ess_e
        
        st.markdown("---")
        st.markdown("**📋 Détail des émissions Scope 1 :**")
        st.write(f"• 🛢️ Diesel : {diesel_e:.2f} kg CO₂")
        st.write(f"• 🔥 Gaz naturel : {gaz_e:.2f} kg CO₂")
        st.write(f"• ⛽ Essence : {ess_e:.2f} kg CO₂")
        st.markdown(f'<div class="result-box">🟦 Total Scope 1 : {scope1:.2f} kg CO₂</div>', unsafe_allow_html=True)

    # Scope 2 - Électricité
    with st.expander("🟨 Scope 2 – Électricité", expanded=True):
        st.markdown("**Émissions indirectes liées à la consommation d'électricité**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            kwh = st.number_input("⚡ Consommation électrique (kWh)", min_value=0.0, value=0.0)
        
        with col2:
            fact_elec = st.number_input("⚡ Facteur électricité (kg CO₂/kWh)", min_value=0.0, value=0.059)
        
        scope2 = kwh * fact_elec
        st.markdown(f'<div class="result-box">🟨 Total Scope 2 : {scope2:.2f} kg CO₂</div>', unsafe_allow_html=True)

    # Scope 3 - Autres émissions
    with st.expander("🟧 Scope 3 – Autres émissions indirectes", expanded=True):
        st.markdown("**Émissions indirectes de la chaîne de valeur**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📊 Quantités**")
            trans_q = st.number_input("🚚 Transport – quantité (km)", min_value=0.0, value=0.0)
            mat_q = st.number_input("🏭 Matières premières – quantité (kg)", min_value=0.0, value=0.0)
            dech_q = st.number_input("🗑️ Déchets – quantité (kg)", min_value=0.0, value=0.0)
        
        with col2:
            st.markdown("**🔢 Facteurs d'émission**")
            trans_f = st.number_input("🚚 Transport – facteur (kg CO₂/km)", min_value=0.0, value=0.12)
            mat_f = st.number_input("🏭 Matières premières – facteur (kg CO₂/kg)", min_value=0.0, value=1.5)
            dech_f = st.number_input("🗑️ Déchets – facteur (kg CO₂/kg)", min_value=0.0, value=0.8)
        
        # Calculs Scope 3
        trans_e = trans_q * trans_f
        mat_e = mat_q * mat_f
        dech_e = dech_q * dech_f
        
        scope3 = trans_e + mat_e + dech_e
        
        st.markdown("---")
        st.markdown("**📋 Détail des émissions Scope 3 :**")
        st.write(f"• 🚚 Transport : {trans_e:.2f} kg CO₂")
        st.write(f"• 🏭 Matières premières : {mat_e:.2f} kg CO₂")
        st.write(f"• 🗑️ Déchets : {dech_e:.2f} kg CO₂")
        st.markdown(f'<div class="result-box">🟧 Total Scope 3 : {scope3:.2f} kg CO₂</div>', unsafe_allow_html=True)
    
    total_general = scope1 + scope2 + scope3

# Section des résultats finaux
st.divider()
st.markdown("## 🎯 Résultats Finaux")

if produit_final:
    st.markdown(f"### 📦 Produit analysé : **{produit_final}**")
else:
    st.markdown("### 📦 Produit analysé : **Non spécifié**")

if mode_analyse == "🧩 Analyse par constituants" and constituants_data:
    # Tableau récapitulatif de tous les constituants
    st.markdown("### 📋 Détail par constituant")
    df_constituants = pd.DataFrame(constituants_data)
    st.dataframe(df_constituants, use_container_width=True)
    
    # Calcul des totaux par scope
    total_scope1 = sum([c['Scope 1 (kg CO₂)'] for c in constituants_data])
    total_scope2 = sum([c['Scope 2 (kg CO₂)'] for c in constituants_data])
    total_scope3 = sum([c['Scope 3 (kg CO₂)'] for c in constituants_data])
    
    # Tableau récapitulatif final
    st.markdown("### 📊 Répartition par scope (assemblage complet)")
    
    data_final = {
        "Scope": ["🟦 Scope 1 - Émissions directes", "🟨 Scope 2 - Électricité", "🟧 Scope 3 - Autres émissions", "🏭 TOTAL ASSEMBLAGE"],
        "Émissions (kg CO₂)": [total_scope1, total_scope2, total_scope3, total_general],
        "Pourcentage (%)": [
            f"{(total_scope1/total_general*100):.1f}" if total_general > 0 else "0.0",
            f"{(total_scope2/total_general*100):.1f}" if total_general > 0 else "0.0",
            f"{(total_scope3/total_general*100):.1f}" if total_general > 0 else "0.0",
            "100.0"
        ]
    }
    
    df_final = pd.DataFrame(data_final)
    st.table(df_final)
    
    # Visualisation
    st.markdown("---")
    st.markdown("### 📈 Visualisation des émissions")
    
    if total_general > 0:
        col_viz1, col_viz2 = st.columns(2)
        
        with col_viz1:
            st.markdown("**📊 Répartition par Scope**")
            chart_data = pd.DataFrame({
                'Scope': ['Scope 1', 'Scope 2', 'Scope 3'],
                'Émissions (kg CO₂)': [total_scope1, total_scope2, total_scope3]
            })
            st.bar_chart(chart_data.set_index('Scope'))
        
        with col_viz2:
            st.markdown("**🧩 Émissions par Constituant**")
            chart_constituants = pd.DataFrame({
                'Constituant': [c['Constituant'] for c in constituants_data],
                'Émissions (kg CO₂)': [c['Total (kg CO₂)'] for c in constituants_data]
            })
            st.bar_chart(chart_constituants.set_index('Constituant'))

elif mode_analyse == "📈 Analyse globale par scopes":
    # Tableau récapitulatif pour le mode global
    data_global = {
        "Scope": ["🟦 Scope 1 - Émissions directes", "🟨 Scope 2 - Électricité", "🟧 Scope 3 - Autres émissions", "🌍 TOTAL GLOBAL"],
        "Émissions (kg CO₂)": [scope1, scope2, scope3, total_general],
        "Pourcentage (%)": [
            f"{(scope1/total_general*100):.1f}" if total_general > 0 else "0.0",
            f"{(scope2/total_general*100):.1f}" if total_general > 0 else "0.0",
            f"{(scope3/total_general*100):.1f}" if total_general > 0 else "0.0",
            "100.0"
        ]
    }
    
    df_global = pd.DataFrame(data_global)
    st.table(df_global)
    
    # Visualisation pour le mode global
    st.markdown("---")
    st.markdown("### 📈 Visualisation des émissions")
    
    if total_general > 0:
        chart_data = pd.DataFrame({
            'Scope': ['Scope 1', 'Scope 2', 'Scope 3'],
            'Émissions (kg CO₂)': [scope1, scope2, scope3]
        })
        st.bar_chart(chart_data.set_index('Scope'))

# Résultat final principal
st.markdown("---")
if total_general > 0:
    st.markdown(f'''
    <div class="result-box" style="background: linear-gradient(135deg, #28a745, #20c997); font-size: 1.5rem;">
        <h2>🏆 Empreinte Carbone Totale</h2>
        <h1>{total_general:.2f} kg CO₂</h1>
        <p>{produit_final if produit_final else 'Produit analysé'}</p>
    </div>
    ''', unsafe_allow_html=True)
else:
    st.info("🔧 Veuillez saisir des données pour voir les résultats.")

# Section d'export
st.markdown("---")
st.markdown('<div class="export-section">', unsafe_allow_html=True)
st.markdown("### 📥 Export des Résultats")

# Préparation des données pour export
if mode_analyse == "🧩 Analyse par constituants" and constituants_data:
    export_data = []
    for c in constituants_data:
        export_data.append({
            "Produit Final": produit_final if produit_final else "Non spécifié",
            "Constituant": c['Constituant'],
            "Poids (kg)": c['Poids (kg)'],
            "Scope 1 (kg CO₂)": c['Scope 1 (kg CO₂)'],
            "Scope 2 (kg CO₂)": c['Scope 2 (kg CO₂)'],
            "Scope 3 (kg CO₂)": c['Scope 3 (kg CO₂)'],
            "Total (kg CO₂)": c['Total (kg CO₂)'],
            "Date": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    # Ajouter la ligne de total
    export_data.append({
        "Produit Final": produit_final if produit_final else "Non spécifié",
        "Constituant": "TOTAL ASSEMBLAGE",
        "Poids (kg)": sum([c['Poids (kg)'] for c in constituants_data]),
        "Scope 1 (kg CO₂)": total_scope1,
        "Scope 2 (kg CO₂)": total_scope2,
        "Scope 3 (kg CO₂)": total_scope3,
        "Total (kg CO₂)": total_general,
        "Date": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    })
else:
    # Export pour le mode global
    export_data = [{
        "Produit": produit_final if produit_final else "Non spécifié",
        "Scope 1 - Émissions directes (kg CO₂)": scope1,
        "Scope 2 - Électricité (kg CO₂)": scope2,
        "Scope 3 - Autres émissions (kg CO₂)": scope3,
        "Total (kg CO₂)": total_general,
        "Date": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    }]

df_export = pd.DataFrame(export_data)

# Bouton de téléchargement
col_export1, col_export2 = st.columns(2)

with col_export1:
    st.download_button(
        label="📥 Télécharger les résultats (CSV)",
        data=df_export.to_csv(index=False, sep=';', decimal=','),
        file_name=f"bilan_carbone_{produit_final.replace(' ', '_') if produit_final else 'produit'}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

with col_export2:
    st.download_button(
        label="📊 Télécharger les résultats (Excel)",
        data=df_export.to_csv(index=False, sep='\t'),
        file_name=f"bilan_carbone_{produit_final.replace(' ', '_') if produit_final else 'produit'}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.tsv",
        mime="text/tab-separated-values"
    )

st.markdown('</div>', unsafe_allow_html=True)

# Informations supplémentaires
st.markdown("---")
st.markdown("""
## 📚 Méthodologie et Informations

### 🔬 Approche Scientifique
- **Analyse par constituants** : Chaque pièce/composant est analysé individuellement selon la méthodologie LCA (Life Cycle Assessment)
- **Assemblage final** : La somme des émissions de tous les constituants donne l'empreinte totale du produit
- **Analyse globale** : Approche consolidée pour une vue d'ensemble rapide

### 🏭 Facteurs d'Émission par Défaut
| Source | Facteur | Unité | Source |
|--------|---------|-------|--------|
| 🛢️ Diesel | 2.68 | kg CO₂/L | Base Carbone |
| 🔥 Gaz naturel | 2.02 | kg CO₂/m³ | Base Carbone |
| ⛽ Essence | 2.31 | kg CO₂/L | Base Carbone |
| ⚡ Électricité (France) | 0.059 | kg CO₂/kWh | RTE |
| 🚚 Transport (route) | 0.12 | kg CO₂/km | Base Carbone |
| 🏭 Matières premières | 1.5 | kg CO₂/kg | Moyenne industrielle |
| 🗑️ Déchets | 0.8 | kg CO₂/kg | Moyenne traitement |

### 🎓 Projet Académique
**École Nationale des Ingénieurs de Monastir**  
TPE combustion réalisé par :  
Halima Bouajina, Nermine Dardouri, Arwa khemira, Rima Yeferni, Ons Selmi

*Vous pouvez modifier ces facteurs selon vos données spécifiques et sources locales*
""")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9rem;'>
    🌍 Calculateur d'Empreinte Carbone - École Nationale des Ingénieurs de Monastir<br>
    © 2026 TPE Combustion - Analyse environnementale
</div>
""", unsafe_allow_html=True)
